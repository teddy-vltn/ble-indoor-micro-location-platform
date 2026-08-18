from flask import jsonify, request
from flask_restx import Resource, fields
from bson import ObjectId

from lib.api import api, send_error, send_success, create_combined_model, send_not_found_error
from lib.models import session_model, error_response, generic_success_response, not_found_error_response
from modules.database.utils.hosts_utils import refresh_hosts_cache
from modules.database.utils.cache_utils import add_to_cache, get_from_cache, get_active_profile_id
from modules.database.utils.profile_utils import duplicate_profile, update_profile_name, delete_profile, create_profile, update_graph_svg
from modules.database.utils.sessions_utils import create_session, get_sessions, mark_session_as_finished, get_session
from modules.database.database import profiles_collection, active_profile_key, active_session_key

# Define namespace
profile_ns = api.namespace('profiles', description='Profile operations')

# Define response models
get_all_sessions_response = api.model('AllSessions', {
    'sessions': fields.List(fields.Nested(session_model), description='List of all sessions')
})

# DuplicateProfile endpoint
@profile_ns.route('/<string:_id>/duplicate')
@api.response(500, 'Error duplicating the profile', model=error_response)
@api.response(200, 'Profile duplicated successfully', model=generic_success_response)
class DuplicateProfile(Resource):
    @api.doc(description='Duplicate the active profile.')
    def post(self, _id):
        """
        Duplicate the active profile.
        """
        result = duplicate_profile(_id)
        if not result:
            return send_error('Erreur lors de la duplication du profile.', code=500)

        return send_success('Profile dupliqué avec succès.')

# Profile endpoint
@profile_ns.route('/<string:_id>')
@api.response(404, 'Profile not found', model=not_found_error_response)
@api.response(409, 'Cannot delete active profile', model=error_response)
@api.response(500, 'Error updating the graph', model=error_response)
@api.response(200, 'Success', model=generic_success_response)
class Profile(Resource):
    @api.doc(description='Modify an existing profile name and update corresponding graph and group.')
    @api.expect(api.model('ProfileUpdate', {
        'new_name': fields.String(required=True, description='New profile name'),
        'graph_svg': fields.String(description='Graph SVG file name')
    }))
    def put(self, _id):
        """
        Modify an existing profile name and update corresponding graph and group.
        """
        data = request.json
        new_profile_name = data['new_name']

        result = update_profile_name(_id, new_profile_name)
        if not result:
            return send_not_found_error('Profile non trouvé.')
        
        graph_svg = data.get('graph_svg')
        if graph_svg:
            result = update_graph_svg(_id, graph_svg)
            if not result:
                return send_error('Erreur lors de la mise à jour du graphique.', code=500)

        return send_success('Profile modifié avec succès.')
    
    @api.doc(description='Delete a profile and its associated graph and group.')
    def delete(self, _id):
        """
        Delete a profile and its associated graph and group.
        """
        profile = profiles_collection.find_one({'_id': ObjectId(_id)})
        if not profile:
            return send_not_found_error('Profile non trouvé.')

        active_profile = get_active_profile_id()
        if active_profile == profile["_id"]:
            return send_error('Impossible de supprimer le profile actif.', code=403)

        result = delete_profile(_id)
        if not result:
            return send_error('Erreur lors de la suppression du profile.', code=500)

        return send_success('Profile supprimé avec succès.')
    
    @api.doc(description='Change the active profile.')
    def patch(self, _id):
        """
        Change the active profile.
        """
        profile = profiles_collection.find_one({'_id': ObjectId(_id)})
        if not profile:
            return send_not_found_error('Profile non trouvé.')

        add_to_cache(active_profile_key, profile["_id"])
        add_to_cache('inventory', {})
        refresh_hosts_cache()

        return send_success('Profile actif modifié avec succès.')

# ProfileList endpoint
@profile_ns.route('')
@api.response(500, 'Error creating the profile', model=error_response)
@api.response(201, 'Profile created successfully', model=generic_success_response)
class ProfileList(Resource):
    @api.doc(description='Create a new profile along with its graph and group.')
    @api.expect(api.model('ProfileCreate', {
        'name': fields.String(required=True, description='Profile name'),
        'graph_svg': fields.String(description='Graph SVG file name')
    }))
    def post(self):
        """
        Create a new profile along with its graph and group.
        """
        data = request.json
        profile_name = data['name']
        graph_svg = data.get('graph_svg', 'map.svg')

        result = create_profile(profile_name, graph_svg)
        if not result:
            return send_error('Erreur lors de la création du profile.', code=500)

        return send_success('Profile créé avec succès.', code=201)

# AddSession endpoint
@profile_ns.route('/<string:_id>/start-session/<string:name>')
@api.response(409, 'Session already active', model=error_response)
@api.response(500, 'Error creating the session', model=error_response)
@api.response(201, 'Session added successfully', model=generic_success_response)
class AddSession(Resource):
    @api.doc(description='Add a new session to the profile.')
    def post(self, _id, name):
        """
        Add a new session to the profile.
        """
        old_session = get_from_cache(active_session_key)
        if old_session:
            return send_error('Une session est déjà active, veuillez la terminer avant d\'en ajouter une nouvelle.', code=409)

        result = create_session(_id, name)
        if not result:
            return send_error('Erreur lors de la création de la session.', code=500)

        add_to_cache(active_session_key, str(result.inserted_id))
        return send_success('Session ajoutée avec succès.', code=201)

# ProfileSessions endpoint
@profile_ns.route('/<string:_id>/sessions')
class ProfileSessions(Resource):
    @api.doc(description='Get all sessions for the profile.')
    @api.marshal_with(create_combined_model(get_all_sessions_response), code=200)
    def get(self, _id):
        """
        Get all sessions for the profile.
        """
        return send_success('Sessions retrieved successfully.', {"sessions": get_sessions(_id)})

@profile_ns.route('/sessions/<string:session_id>')
@api.response(404, 'Session not found', model=error_response)
class ProfileSession(Resource):
    @api.doc(description='Get the session by ID.')
    @api.marshal_with(create_combined_model(session_model), code=200)
    def get(self, session_id):
        """
        Get the session by ID.
        """
        session = get_session(session_id)
        if not session:
            return send_not_found_error('Session non trouvée.')

        return send_success('Session retrieved successfully.', session)

# FinishSession endpoint
@profile_ns.route('/finish-active-session')
@api.response(404, 'No active session found', model=error_response)
@api.response(500, 'Error finishing the session', model=error_response)
@api.response(200, 'Session finished successfully', model=generic_success_response)
class FinishSession(Resource):
    @api.doc(description='Mark the active session as finished.')
    def put(self):
        """
        Mark the active session as finished.
        """
        session_id = get_from_cache(active_session_key)
        if not session_id:
            return send_not_found_error('Aucune session active trouvée.')

        result = mark_session_as_finished(session_id)
        if not result:
            return send_error('Erreur lors de la fin de la session.', code=500)

        add_to_cache(active_session_key, None)
        return send_success('Session terminée avec succès.')
