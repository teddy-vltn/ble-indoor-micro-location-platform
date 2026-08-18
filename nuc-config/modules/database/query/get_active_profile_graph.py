from bson.objectid import ObjectId
from modules.database.database import profiles_collection, graphs_collection, transform_objectids_to_string
from modules.database.utils.cache_utils import get_active_profile_id

def get_active_profile_graph():
    
    active_profile_id = get_active_profile_id()

    if not active_profile_id:
        return None
    
    # Find the graph alone 
    profile_graph = profiles_collection.find_one({'_id': ObjectId(active_profile_id)}, {'graph_id': 1})

    if not profile_graph:
        return None
    
    graph_id = profile_graph['graph_id']
    
    graph = graphs_collection.find_one({'_id': ObjectId(graph_id)}, {'_id': 1, 'nodes': 1, 'edges': 1})

    return transform_objectids_to_string(graph) or {}