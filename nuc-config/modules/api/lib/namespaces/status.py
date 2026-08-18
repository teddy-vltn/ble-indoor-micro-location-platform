import gzip

from flask import json, make_response
from flask_restx import Resource, fields

from lib.models import profile_model, session_model, graph_model, host_cache_model, generic_success_response

from modules.database.utils.cache_utils import get_from_cache
from modules.database.query.get_active_profile import get_active_profile
from modules.database.query.get_active_session import get_active_session
from modules.database.query.get_active_profile_group import get_active_profile_group
from modules.database.query.get_active_profile_graph import get_active_profile_graph
from modules.database.query.get_active_session_players import get_session_players
from modules.database.query.get_all_profiles import get_all_profiles
from modules.database.utils.hosts_utils import remove_ghost_hosts
from modules.database.utils.ansible_utils import find_all_ansible_logs
from lib.api import api, send_success

status_ns = api.namespace('status', description='Status operations')

def get_inventory():
    """Retrieve the current inventory of hosts, ensuring it is up-to-date."""
    groups = get_active_profile_group()
    if not groups:
        return {}

    remove_ghost_hosts()
    inventory = get_from_cache('inventory')
    hosts = groups['hosts']

    for host in hosts:
        name = host['name']
        inventory[name] = inventory.get(name, {
            "name": name,
            "active": host.get('active', False),
            "node": host.get('node', ''),
            "online": False,
            "services": {},
            "last_pings": [],
            "timestamp_last_successful_ping": inventory.get(name, {}).get('timestamp_last_successful_ping', None)
        })
        inventory[name]['active'] = host.get('active', False)
        inventory[name]['node'] = host.get('node', '')
        inventory[name]['_id'] = host['_id']

    return {k: inventory[k] for k in sorted(inventory)}

def get_players():
    return get_session_players()

def get_ansible():
    return find_all_ansible_logs()

def get_graph():
    return get_active_profile_graph(),

def encode_to_gzip(data):
    content = json.dumps(data).encode('utf-8')
    response = make_response(gzip.compress(content, 5))
    response.headers['Content-Encoding'] = 'gzip'
    response.headers['Content-Length'] = len(response.data)
    response.headers['Content-Type'] = 'application/json'
    return response
    
status_response = api.model('StatusResponse', {
    'active_profile': fields.Nested(profile_model, description='Active profile'),
    'active_session': fields.Nested(session_model, description='Active session'),
    'all_profiles': fields.List(fields.Nested(profile_model), description='List of all profiles'),
    'inventory': fields.List(fields.Nested(host_cache_model), description='Inventory of hosts'),
    'ansible': fields.Raw(description='Ansible logs'),
    'graph': fields.Nested(graph_model, description='Active profile graph')
})

@status_ns.route('')
class Status(Resource):
    @api.doc(description='Get the status of the active profile, session, and inventory')
    @api.response(200, 'Success', status_response)
    def get(self):
        return encode_to_gzip({
            'active_profile': get_active_profile(),
            'active_session': get_active_session(),
            'all_profiles': get_all_profiles(),
            'inventory': get_inventory(),
            'ansible': get_ansible(),
            'graph': get_graph(),
            'hosts_names': get_from_cache('hosts_names')
        })

# Check health of the API
@api.route('/health')
class Health(Resource):
    @api.doc(description='Check the health of the API')
    @api.response(200, 'Success', generic_success_response)
    def get(self):
        return send_success('API is healthy')
