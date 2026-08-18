from modules.database.database import cache_collection, active_profile_key, active_session_key
from bson.objectid import ObjectId

def add_to_cache(key, value):
    """
    Add or update a value in the cache by key.

    Args:
        key (str): The key to store the value under.
        value (Any): The value to store in the cache.

    """
    # Update the cache_collection document with the key and value.
    # If the document does not exist, insert a new document.
    cache_collection.update_one(
        {'key': key},  # The query to match the document to update
        {'$set': {'value': value}},  # The update operation to perform
        upsert=True  # Insert a new document if the query does not match any documents
    )

def get_from_cache(key):
    """
    Retrieve a value from the cache by key.

    Args:
        key (str): The key to retrieve the value for.

    Returns:
        The value associated with the key if found, None otherwise.
    """
    # Query the cache_collection for a document with the specified key
    result = cache_collection.find_one({'key': key})
    
    # If a document is found, return its value, else return None
    if result:
        return result['value']
    return None

def get_active_profile_id():
    """
    Retrieve the active profile ID from the cache.

    This function retrieves the active profile ID from the cache by querying
    the cache collection with the key 'active_profile_key'. The function returns
    the value associated with the key if found, or None if the key is not found.

    Returns:
        The active profile ID if found, None otherwise.
    """
    return get_from_cache(active_profile_key)

def set_active_profile(profile_key, profile_id):
    """
    Set the active profile in the cache.

    Args:
        profile_key (str): The key to associate with the active profile ID.
        profile_id (bson.ObjectId or str): The ID of the active profile.
    """
    # Make sure the profile_id is an ObjectId
    if not isinstance(profile_id, ObjectId):
        profile_id = ObjectId(profile_id)

    # Add the profile ID to the cache, using the provided key
    add_to_cache(profile_key, profile_id)

def get_active_session_id():
    """
    Retrieve the active session ID from the cache.

    This function retrieves the active session ID from the cache by querying
    the cache collection with the key 'active_session_key'. The function returns
    the value associated with the key if found, or None if the key is not found.

    Returns:
        The active session ID if found, None otherwise.
    """
    # Query the cache_collection for a document with the specified key
    return get_from_cache(active_session_key)

def set_active_session(session_key, session_id):
    """
    Set the active session in the cache.

    Args:
        session_key (str): The key to associate with the active session ID.
        session_id (bson.ObjectId or str): The ID of the active session.
    """
    # Ensure the session_id is an ObjectId
    session_id = ObjectId(session_id) if not isinstance(session_id, ObjectId) else session_id

    # Add the session ID to the cache, using the provided key
    add_to_cache(session_key, session_id)
