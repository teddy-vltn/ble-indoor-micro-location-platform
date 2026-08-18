from bson.objectid import ObjectId
from modules.database.database import profiles_collection, groups_collection, hosts_collection, transform_objectids_to_string
from modules.database.utils.cache_utils import get_active_profile_id

def get_active_profile_group():

    active_profile_id = get_active_profile_id()

    if not active_profile_id:
        return None

    # Find the group alone
    profile_group = profiles_collection.find_one({'_id': ObjectId(active_profile_id)}, {'_id': 1, 'group_id': 1})

    if not profile_group:
        return None

    group_id = profile_group['group_id']
    group = groups_collection.find_one({'_id': ObjectId(group_id)}, {'_id': 1, 'hosts': 1})

    if not group:
        return None

    # Populate hosts
    host_ids = group.get('hosts', [])
    if not host_ids:
        group['hosts'] = []
        return group
    
    hosts = list(hosts_collection.find({'_id': {'$in': host_ids}}))

    # Replace ObjectId references with host documents
    group['hosts'] = hosts

    return transform_objectids_to_string(group) or {}
