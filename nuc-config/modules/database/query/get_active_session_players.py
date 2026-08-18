from bson.objectid import ObjectId
from modules.database.database import players_collection, transform_objectids_to_string
from modules.database.utils.cache_utils import get_active_session_id

def get_active_session_players():
    
    active_session_id = get_active_session_id()

    if not active_session_id:
        return {}
    
    # Find the players based on the active sessions id
    players = list(players_collection.find({'session_id': ObjectId(active_session_id), 'has_finished': False}))

    if not players:
        return {}
    
    # Convert ObjectId to string
    for player in players:
        player = transform_objectids_to_string(player)
    
    return players or {}

def get_session_players(session_id):
    """Retrieve all players for a session."""
    players = list(players_collection.find({'session_id': ObjectId(session_id)}))
    if not players:
        return []
    
    for player in players:
        transform_objectids_to_string(player)
    
    return players
