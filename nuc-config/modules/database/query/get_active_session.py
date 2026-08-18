
from modules.database.utils.cache_utils import get_active_session_id
from modules.database.database import sessions_collection, players_collection, transform_objectids_to_string

from bson.objectid import ObjectId

def get_active_session():
    active_session_id = get_active_session_id()

    if not active_session_id:
        return None
    
    result = sessions_collection.find_one({'_id': ObjectId(active_session_id)}) or {}

    players = result.get('players', [])

    # find all players in the active session
    players = players_collection.find({'_id': {'$in': players}})

    result['players'] = list(players)

    return transform_objectids_to_string(result) or {}

    
    


    