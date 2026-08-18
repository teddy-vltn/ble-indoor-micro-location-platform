from bson import ObjectId

from modules.database.database import players_collection
from modules.database.utils.cache_utils import get_active_session_id
from modules.database.utils.sessions_utils import remove_player_from_session, reset_session_players
from datetime import datetime

def create_player(id_minor, devices=[], active_session_id=None):
    """
    Creates a new player in the database.

    Args:
        id_minor (int): The ID of the minor associated with the player.
        devices (list, optional): List of devices associated with the player. Defaults to [].
        active_session_id (str, optional): The ID of the active session. Defaults to None.

    Returns:
        ObjectId: The ID of the newly created player.

    Raises:
        None
    """
    # Check if a session already exists for this player
    # If player exists and has not finished the session, return False
    player = players_collection.find_one({
                                          'id_minor': id_minor, 
                                          'session_id': ObjectId(active_session_id), 
                                          'has_finished': False
                                        })
    if player:
        return False
    
    # Increment the number of players in the session
    id_player = players_collection.count_documents({'session_id': ObjectId(active_session_id)}) + 1

    # Create a new player object
    player = {
        'id_player': id_player,
        'id_minor': id_minor,
        'devices': devices,
        'session_id': ObjectId(active_session_id) if active_session_id else None,
        'started_at': datetime.now().timestamp(),
        'updated_at': datetime.now().timestamp(),
        'has_visited': [],
        'temporal_sequence_visited': {},
        'has_finished': False
    }

    # Insert the player into the database
    player = players_collection.insert_one(player)

    return player.inserted_id

def delete_player(player_id):
    """
    Delete a player by player ID.

    Args:
        player_id (str): The ID of the player to delete.

    Returns:
        bool: True if the player was successfully deleted, False otherwise.
    """
    # Get the player
    # _id is a unique identifier for a document in MongoDB
    # ObjectId is a class to work with MongoDB ObjectIds
    player = players_collection.find_one({'_id': ObjectId(player_id)})

    # If the player does not exist, return False
    if not player:
        return False
    
    # Remove the player from the session
    # If the player is in a session, remove the player from the session
    if player['session_id']:
        remove_player_from_session(player['session_id'], player_id)

    # Delete the player from the players collection
    players_collection.delete_one({'_id': player['_id']})

    # Return True if the player was successfully deleted
    return True

def search_players(id_player=None, id_minor=None, device=None, session_id=None):
    """
    Find a player by id, minor or device.

    Args:
        id_player (int, optional): The ID of the player.
        id_minor (int, optional): The ID of the minor.
        device (str, optional): The device ID.
        session_id (str, optional): The ID of the session.

    Returns:
        Cursor or None: A cursor with the matching players, or None if no players are found.
    """
    # Get the active session ID if not provided
    session_id = session_id or get_active_session_id()
    
    # If no session ID is found, return None
    if not session_id:
        return None

    # Generate the query based on the parameters
    query = {'session_id': ObjectId(session_id), 'has_finished': False}
    
    # Add the ID player parameter to the query if provided
    if id_player:
        query['id_player'] = id_player
    
    # Add the ID minor parameter to the query if provided
    if id_minor:
        query['id_minor'] = id_minor
    
    # Add the device parameter to the query if provided
    if device:
        query['devices'] = { '$in': [device] }

    # Find the players in the players collection that match the query
    players = players_collection.find(query)

    # If no players are found, return None
    if not players:
        return None
    
    # Return the cursor with the matching players
    return players

def add_device_to_player(player_id, device):
    """
    Add a device to a player.

    Args:
        player_id (str): The ID of the player.
        device (str): The device ID.

    Returns:
        bool: True if the device was successfully added to the player, False otherwise.
    """
    # Find the player in the players collection by ID
    player = players_collection.find_one({'_id': ObjectId(player_id)})
    
    # If the player is not found, return False
    if not player:
        return False

    # Add the device to the player's devices list
    player['devices'].append(device)
    
    # Update the player's updated_at field with the current timestamp
    player['updated_at'] = datetime.now().timestamp()
    
    # Replace the player in the players collection with the updated player
    players_collection.replace_one({'_id': ObjectId(player_id)}, player)

    # Return True to indicate that the device was successfully added to the player
    return True

def get_player(player_id):
    """
    Get a player by id.

    Args:
        player_id (str): The ID of the player.

    Returns:
        dict or None: The player document if found, otherwise None.
    """
    # Find the player in the players collection by ID
    player = players_collection.find_one({'_id': ObjectId(player_id)})
    
    # If the player is not found, return None
    if not player:
        return None

    # Return the player document
    return player

def get_all_players(session_id=None):
    """
    Get all players in the session.

    Args:
        session_id (str, optional): The ID of the session. If not provided, the active session ID is used.

    Returns:
        list: A list of player documents.
    """
    # Get the active session ID if not provided
    session_id = session_id or get_active_session_id()
    
    # If no session ID is found, return an empty list
    if not session_id:
        return []

    # Find all players in the session
    players = players_collection.find({'session_id': ObjectId(session_id)})

    # Return the list of player documents
    return list(players)

def delete_all_players(session_id=None):
    """
    Delete all players in a session.

    Args:
        session_id (str, optional): The ID of the session. If not provided, the active session ID is used.

    Returns:
        int: The number of players deleted.
    """
    # Get the session ID, defaulting to the active session ID
    session_id = session_id or get_active_session_id()
    
    # If no session ID is found, return False
    if not session_id:
        return False
    
    # Remove all players from the session
    reset_session_players(session_id)
    
    # Delete all players in the session
    result = players_collection.delete_many({'session_id': ObjectId(session_id)})

    # Return the number of players deleted
    return result.deleted_count
    
def mark_player_has_finished(player_id):
    """
    Mark a player as finished.

    Args:
        player_id (str): The ID of the player.

    Returns:
        bool: True if the player was marked as finished, False otherwise.
    """
    # Find the player in the players collection by ID
    player = players_collection.find_one({'_id': ObjectId(player_id)})
    
    # If the player is not found, return False
    if not player:
        return False

    # Mark the player as finished
    player['has_finished'] = True
    
    # Update the player's updated_at field with the current timestamp
    player['updated_at'] = datetime.now().timestamp()
    
    # Replace the player in the players collection with the updated player
    players_collection.replace_one({'_id': ObjectId(player_id)}, player)

    # Return True to indicate that the player was marked as finished
    return True

def has_player_visited_nodes(player_id, nodes):
    """
    Check if a player has visited the given list of nodes.

    Args:
        player_id (str): The ID of the player.
        nodes (List[str]): The list of nodes to check.

    Returns:
        bool or None: True if the player has visited all the nodes, False if the player has not visited any of the nodes, None if the player does not exist.
    """
    # Find the player in the players collection by ID
    player = players_collection.find_one({'_id': ObjectId(player_id)})
    
    # If the player is not found, return None
    if not player:
        return None

    # Check if the player has visited all the nodes
    for node in nodes:
        if node not in player['has_visited']:
            return False

    # Return True if the player has visited all the nodes
    return True


