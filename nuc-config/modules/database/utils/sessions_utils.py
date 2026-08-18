from modules.database.database import sessions_collection, profiles_collection, players_collection, transform_objectids_to_string
from bson.objectid import ObjectId

from datetime import datetime

def create_session(profile_id, name):
    """Create a new session."""
    # started_at, finished_at, players
    session = {
        'profile_id': ObjectId(profile_id),
        'name': name,
        'started_at': datetime.now().timestamp(),
        'finished_at': None,
        'players': []
    }

    result = sessions_collection.insert_one(session)
    if not result:
        return None
    
    # Add the session to the profile
    profile = profiles_collection.find_one({'_id': ObjectId(profile_id)})

    if not profile:
        return None
    
    profile['sessions'].append(result.inserted_id)
    profiles_collection.update_one({'_id': ObjectId(profile_id)}, {'$set': {'sessions': profile['sessions']}})

    return result

def get_sessions(profile_id):
    """Retrieve all sessions for a profile."""
    sessions = list(sessions_collection.find({'profile_id': ObjectId(profile_id)}))
    if not sessions:
        return []

    # Populate the players
    for session in sessions:
        session_players_ids = session['players']
        session_players = list(players_collection.find({'_id': {'$in': session_players_ids}}))

        session['players'] = session_players

    if not sessions:
        return []
    
    for session in sessions:
        transform_objectids_to_string(session)

    return sessions

def get_session(session_id):
    """Retrieve a session by id."""
    session = sessions_collection.find_one({'_id': ObjectId(session_id)})
    if not session:
        return None
    
    # Populate the players
    session_players_ids = session['players']
    session_players = list(players_collection.find({'_id': {'$in': session_players_ids}}))

    session['players'] = session_players

    return transform_objectids_to_string(session)

def mark_session_as_finished(session_id):
    """Mark a session as finished."""
    sessions_collection.update_one({'_id': ObjectId(session_id)}, {'$set': {'finished_at': datetime.now().timestamp()}})
    return True

def add_player_to_session(session_id, player_id):
    """Add a player to a session."""
    session = sessions_collection.find_one({'_id': ObjectId(session_id)})
    if not session:
        return False

    if player_id not in session['players']:
        session['players'].append(player_id)
        sessions_collection.update_one({'_id': ObjectId(session_id)}, {'$set': {'players': session['players']}})
        return True

    return False

def remove_player_from_session(session_id, player_id):
    """Remove a player from a session."""
    session = sessions_collection.find_one({'_id': ObjectId(session_id)})
    if not session:
        return False

    if player_id in session['players']:
        session['players'].remove(player_id)
        sessions_collection.update_one({'_id': ObjectId(session_id)}, {'$set': {'players': session['players']}})
        return True

    return False

def reset_session_players(session_id):
    """Reset the players in a session."""
    sessions_collection.update_one({'_id': ObjectId(session_id)}, {'$set': {'players': []}})
    return True

def delete_sessions(session_ids):
    """Delete multiple sessions by id."""
    result = sessions_collection.delete_many({'_id': {'$in': [ObjectId(session_id) for session_id in session_ids]}})
    return result.deleted_count