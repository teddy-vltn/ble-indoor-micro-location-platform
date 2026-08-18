from flask import request
from flask_restx import Resource

from lib.api import api, send_error, send_success, create_combined_model, send_not_found_error
from lib.models import group_host_model, error_response, generic_success_response, not_found_error_response, inventory_model
from modules.database.database import groups_collection, hosts_collection

from modules.database.utils.hosts_utils import refresh_hosts_cache
from modules.database.utils.cache_utils import add_to_cache, get_from_cache
from modules.database.query.get_active_profile_group import get_active_profile_group

from bson import ObjectId

inventory_ns = api.namespace('inventory', description='Inventory operations')

update_dict_prompt = {
    'name': 'Nom',
    'active': 'Actif',
    'node': 'Node'
}

@inventory_ns.route('/hosts')
@api.response(404, 'Host not found', model=not_found_error_response)
@api.response(400, 'Invalid host data', model=error_response)
@api.response(200, 'Success', model=generic_success_response)
class GroupHostList(Resource):
    @api.expect(group_host_model)
    def post(self):
        """Add a new host to the group in the active profile."""
        group = get_active_profile_group()
        group_id = group['_id']

        host_data = request.json

        if not host_data or not host_data.get('name'):
            return send_error('Nom de l\'hôte manquant', code=400)

        name = host_data['name']
        active = False
        node = ""

        # Validate and add host
        error, code = validate_host(host_data)
        if error:
            return send_error(error, code=code)

        # Insert host into hosts collection
        new_host = hosts_collection.insert_one({
            'name': name,
            'active': active,
            'node': node
        })
        host_id = new_host.inserted_id

        hosts_names = get_from_cache('hosts_names')
        
        if not hosts_names:
            hosts_names = [ name ]
        else:
            # Check if host name already exists
            if not name in hosts_names:
                hosts_names.append(name)

        add_to_cache('hosts_names', hosts_names)

        # Update group to include new host's ObjectId
        groups_collection.update_one(
            {'_id': ObjectId(group_id)},
            {'$push': {'hosts': host_id}}
        )

        refresh_hosts_cache()

        return send_success(
            'Hôte ajouté au groupe dans le profil actif'
        )
    
    @api.doc(description='Get all hosts in the active profile group.')
    @api.marshal_with(create_combined_model(inventory_model), code=200)
    def get(self):
        """Get all hosts in the active profile group."""
        return send_success('Liste des hôtes récupérée avec succès', get_active_profile_group())

@inventory_ns.route('/hosts/<string:_id>')
@api.response(404, 'Host not found', model=not_found_error_response)
@api.response(400, 'Invalid host data', model=error_response)
@api.response(200, 'Success', model=generic_success_response)
class GroupHost(Resource):
    @api.doc(description='Update the host in the active profile group.')
    @api.expect(group_host_model)
    def put(self, _id):
        """Update the host in the active profile group."""
        group = get_active_profile_group()
        group_id = group['_id']

        host_data = request.json

        # Validate host data if necessary
        error, code = validate_host(host_data, _id)
        if error:
            return send_error(error, code=code)

        # If node needs to be updated, find if the node is not already attributed to another host
        # If it is, remove the node from the other host
        if 'node' in host_data:
            node = host_data['node']
            if node:
                existing_host_with_node = hosts_collection.find_one({'node': node})
                if existing_host_with_node and str(existing_host_with_node['_id']) != _id:
                    hosts_collection.update_one(
                        {'_id': existing_host_with_node['_id']},
                        {'$set': {'node': None}}
                    )

        # Build the update dictionary dynamically based on provided data
        update_dict = {key: value for key, value in host_data.items() if key in group_host_model.keys()}

        # Perform the database update
        hosts_collection.update_one(
            {'_id': ObjectId(_id)},
            {'$set': update_dict}
        )

        # Get prompt for updated fields to return in the response
        prompt = {key: update_dict_prompt[key] for key in update_dict.keys()}

        refresh_hosts_cache()

        message_with_prompt = ', '.join([f'{prompt[key]}: {value}' for key, value in update_dict.items()])
        return send_success(
            ' '.join(['Hôte mis à jour:', message_with_prompt]),
        )

    @api.doc(description='Delete the host from the active profile group.')
    def delete(self, _id):
        """Delete the host from the active profile group."""
        group = get_active_profile_group()
        group_id = group['_id']

        # Remove host from hosts collection
        host = hosts_collection.find_one({'_id': ObjectId(_id)})
        if not host:
            return send_not_found_error('Hôte non trouvé')

        hosts_collection.delete_one({'_id': ObjectId(_id)})

        # Remove host reference from the group
        result = groups_collection.update_one(
            {'_id': ObjectId(group_id)},
            {'$pull': {'hosts': ObjectId(_id)}}
        )

        if result.matched_count == 0:
            return send_not_found_error('Hôte non trouvé dans le groupe')

        refresh_hosts_cache()

        return send_success(
            'L\'hôte {} a été supprimé du groupe dans le profil actif'.format(_id),
        )

# Validate the host data before posting a new host
def validate_host(host_data, host_id=None):
    # Check if the host name is unique or not empty and contains only alphanumeric characters
    name = host_data.get('name')
    #if not name or name == "" and not host_id:
        #return 'Nom de l\'hôte invalide', 400
     
    hosts = get_active_profile_group().get('hosts', {})

    # Check if the host already exists in the group
    for host in hosts:
        if str(host['_id']) == host_id:
            continue
        if host['name'] == name:
            return 'Nom de l\'hôte déjà utilisé', 409

    return None, None

