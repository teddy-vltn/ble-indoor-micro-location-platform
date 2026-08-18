from flask import request
from flask_restx import Resource, fields

from lib.api import send_error, send_success, create_combined_model, send_missing_params_error, send_not_found_error
from lib.models import session_model_create, has_visited_model, player_model, error_response, generic_success_response, not_found_error_response

from modules.database.database import transform_objectids_to_string
from modules.database.utils.cache_utils import get_active_session_id  
from modules.database.utils.players_utils import (
    create_player, delete_player, search_players, get_player, 
    delete_all_players, mark_player_has_finished, has_player_visited_nodes, get_all_players,
    add_device_to_player
)
from modules.database.utils.sessions_utils import add_player_to_session

from lib.api import api

# Define namespace
sessions_ns = api.namespace('players', description='Session operations')

# Define response models
post_player_response = api.model('PostPlayer', {
    'player_id': fields.String(description='Player ID'),
    'session_id': fields.String(description='Active session ID')
})

get_all_players_response = api.model('AllPlayers', {
    'players': fields.List(fields.Nested(player_model), description='List of all players')
})

# Define query parameters for finding a player
player_query_params = {
    'id_player': {'description': 'ID of the user', 'type': 'integer'},
    'id_minor': {'description': 'ID of the minor', 'type': 'integer'},
    'device': {'description': 'Device ID', 'type': 'string'}
}

session_query_params_optional = {
    'session_id': {'description': 'ID of the session (if empty return the active session)', 'type': 'string', 'required': False}
}

visited_nodes_response = api.model('VisitedNodes', {
    'visited': fields.Boolean(description='Whether the player has visited the nodes', required=True)
})

add_device_model = api.model('AddDevice', {
    'device': fields.String(description='Device ID', required=True)
})

search_players_response = api.model('SearchPlayers', {
    'players': fields.List(fields.Nested(player_model), description='List of players')
})

player_query_and_session_params = {**player_query_params, **session_query_params_optional}

# PlayerSession endpoint
@sessions_ns.route('')
@api.response(404, 'Session not found', model=not_found_error_response)
@api.response(409, 'Player already exists in the session', model=error_response)
class PlayerSession(Resource):
    @api.doc(description='Create a new player and add it to the active session')
    @api.expect(session_model_create)
    @api.marshal_with(create_combined_model(post_player_response), code=200)
    def post(self):
        """
        Create a new player and add it to the active session.
        """
        session_data = request.json

        id_minor = session_data['id_minor']
        devices = session_data['devices'] if 'devices' in session_data else []

        active_session_id = get_active_session_id()
        if not active_session_id:
            return send_not_found_error('Active session not found')

        result = create_player(id_minor, devices, active_session_id)
        if not result:
            return send_error('Player already exists in the session', code=409)
        
        add_player_to_session(active_session_id, result)

        return send_success('Player has been created and added to the session', {
            'player_id': str(result),
            'session_id': active_session_id
        })
    
    @api.doc(params=session_query_params_optional, description='Get all players in a session')
    @api.marshal_with(create_combined_model(get_all_players_response), code=200)
    def get(self):
        """
        Get all players in a session.
        """
        session_id = request.args.get('session_id', type=str)
        players = get_all_players(session_id=session_id)
        return send_success('Players retrieved successfully', {'players': players})

# Session endpoint
@sessions_ns.route('/<string:_id>')
@api.response(404, 'Session not found', model=error_response)
@api.response(200, 'Player retrieved successfully', model=generic_success_response)
class Session(Resource):
    @api.marshal_with(create_combined_model(player_model), code=200)
    def get(self, _id):
        """
        Get player details by player ID.
        """
        player = get_player(_id)
        if not player:
            return send_not_found_error('Player not found')

        return send_success('Player retrieved successfully', transform_objectids_to_string(player))

    def delete(self, _id):
        """
        Delete a player by player ID.
        """
        result = delete_player(_id)

        if not result:
            return send_not_found_error('Player not found')

        return send_success('Session deleted')
    
@sessions_ns.route('/<string:_id>/add-device/<string:device>')
@api.response(404, 'Session not found', model=error_response)
@api.response(200, 'Device added to player', model=generic_success_response)
class AddDevice(Resource):
    @api.doc(description='Add a device to a player')
    def put(self, _id, device):
        """
        Add a device to a player.
        """
        result = add_device_to_player(_id, device)

        if not result:
            return send_not_found_error('Player not found')

        return send_success('Device added to player')

# FindSession endpoint
@sessions_ns.route('/search')
@api.response(400, 'At least one parameter is missing', model=error_response)
@api.response(404, 'No player found', model=not_found_error_response)
class FindSession(Resource):
    @api.doc(params=player_query_and_session_params, description='Search for players based on id_player, id_minor, and device')
    @api.marshal_with(create_combined_model(search_players_response), code=200)
    def get(self):
        """
        Search for players based on id_player, id_minor, and device.
        """
        id_player = request.args.get('id_player', type=int) or None
        id_minor = request.args.get('id_minor', type=int) or None
        device = request.args.get('device', type=str) or None

        session_id = request.args.get('session_id', type=str)

        if id_minor is None and device is None and id_player is None:
            return send_missing_params_error(['id_player', 'id_minor', 'device'])

        players = list(search_players(
            id_player=id_player, 
            id_minor=id_minor, 
            device=device, 
            session_id=session_id
        ))

        if not players:
            return send_not_found_error('No player found')
        
        players_len = str(len(players))

        return send_success(players_len + " players found.", { 'players': transform_objectids_to_string(players) })

# WipeSessions endpoint
@sessions_ns.route('/wipe-players')
@api.response(404, 'No players found', model=not_found_error_response)
@api.response(200, 'Players deleted', model=generic_success_response)
class WipeSessions(Resource):
    @api.doc(params=session_query_params_optional, description='Delete all players from a session')
    def delete(self):
        """
        Delete all players from a session.
        """
        session_id = request.args.get('session_id', type=str)

        result = delete_all_players(session_id=session_id)
        if not result:
            return send_not_found_error('No players found')

        return send_success(f'{result} players deleted')

# FinishSession endpoint
@sessions_ns.route('/<string:_id>/finish')
@api.response(404, 'Session not found', model=not_found_error_response)
@api.response(200, 'Session finished', model=generic_success_response)
class FinishSession(Resource):
    def put(self, _id):
        """
        Mark a player session as finished.
        """
        result = mark_player_has_finished(_id)

        if not result:
            return send_not_found_error('Player not found')

        return send_success('Session finished')

# HasVisited endpoint
@sessions_ns.route('/<string:_id>/has-visited')
@api.response(404, 'Session not found', model=not_found_error_response)
class HasVisited(Resource):
    @api.expect(has_visited_model)
    @api.marshal_with(create_combined_model(visited_nodes_response), code=200)
    def post(self, _id):
        """
        Check if a player has visited certain nodes.
        """
        data = request.json
        nodes = data['nodes']
        
        result = has_player_visited_nodes(_id, nodes)
        if result is None:
            return send_not_found_error('Player not found')

        return send_success('Visited nodes checked', {'visited': result})
