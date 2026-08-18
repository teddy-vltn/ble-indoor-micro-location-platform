from modules.database.database import profiles_collection
from modules.database.utils.graphs_utils import create_graph, duplicate_graph, delete_graph
from modules.database.utils.groups_utils import create_group, duplicate_group, delete_group
from modules.database.utils.sessions_utils import delete_sessions
#modules.database.utils.players_utils import duplicate_all_players
from datetime import datetime

from bson import ObjectId

def create_profile(name, graph_svg='map.svg'):
    """Create a new profile with the specified name."""
    created_at = datetime.now().timestamp()
    updated_at = created_at

    # Create a graph and group for the new profile
    graph = create_graph()
    group = create_group()

    result = profiles_collection.insert_one({
        'name': name,
        'created_at': created_at,
        'updated_at': updated_at,
        'graph_id': graph.inserted_id,
        'group_id': group.inserted_id,
        'graph_svg': graph_svg,
        'sessions': []
    })

    if not result:
        return None

    return result

def update_profile_name(_id, name):
    """Update the name of the profile with the specified ID."""
    updated_at = datetime.now().timestamp()

    result = profiles_collection.update_one({'_id': ObjectId(_id)}, {'$set': {'name': name, 'updated_at': updated_at}})
    if not result:
        return False

    return True

def update_graph_svg(_id, graph_svg):
    """Update the graph svg of the profile with the specified ID."""
    updated_at = datetime.now().timestamp()

    result = profiles_collection.update_one({'_id': ObjectId(_id)}, {'$set': {'graph_svg': graph_svg, 'updated_at': updated_at}})
    if not result:
        return False

    return True

def delete_profile(_id):
    """Delete the profile with the specified ID."""
    # Find the profile to delete
    profile = profiles_collection.find_one({'_id': ObjectId(_id)})
    if not profile:
        return False

    # Delete the graph and group associated with the profile
    delete_graph(profile['graph_id'])
    delete_group(profile['group_id'])

    # Delete all the logs associated with the profile
    #delete_all_ansible_logs(_id)

    # Delete all the players associated with the profile
    #delete_all_players(_id)

    # Delete all the sessions associated with the profile
    sessions_ids = [str(session_id) for session_id in profile['sessions']]
    if profile['sessions'] and len(sessions_ids) > 0:
        delete_sessions(sessions_ids)

    # Delete the profile
    profiles_collection.delete_one({'_id': ObjectId(_id)})

    return True

def duplicate_profile(_id):

    # Find the profile to duplicate
    profile_to_duplicate = profiles_collection.find_one({'_id': ObjectId(_id) })
    name = profile_to_duplicate['name']

    if not profile_to_duplicate:
        return None
    
    new_profile_name = f"{name}_copy"

    i = 1
    MAX_TRIES = 100
    for _ in range(MAX_TRIES):
        if not profiles_collection.find_one({'name': new_profile_name}):
            break
        new_profile_name = f"{new_profile_name}_copy_{i}"
        i += 1
        if i > MAX_TRIES:
            return None

    created_at = datetime.now().timestamp()
    updated_at = created_at
    graph_svg = profile_to_duplicate['graph_svg']

    # Get the graph and group of the profile to duplicate
    graph = profile_to_duplicate['graph_id']
    group = profile_to_duplicate['group_id']

    # Duplicate the graph and group
    new_graph = duplicate_graph(graph)
    new_group = duplicate_group(group)

    if not new_graph or not new_group:
        return None
    
    result = profiles_collection.insert_one({
        'name': new_profile_name,
        'created_at': created_at,
        'updated_at': updated_at,
        'graph_id': new_graph.inserted_id,
        'group_id': new_group.inserted_id,
        'graph_svg': graph_svg,
        'sessions': []
    })

    if not result:
        return None
    
    #result_id = result.inserted_id

    # Duplicate all the logs associated with the profile
    #duplicate_all_ansible_logs(profile_to_duplicate['_id'], result_id)

    # Duplicate all the players associated with the profile
    #duplicate_all_players(profile_to_duplicate['_id'], result_id)
    
    return result






