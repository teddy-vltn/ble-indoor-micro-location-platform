
from modules.database.utils.cache_utils import get_active_profile_id
from modules.database.database import profiles_collection, transform_objectids_to_string
from modules.database.utils.sessions_utils import get_sessions

from bson.objectid import ObjectId

def get_active_profile():
    active_profile_id = get_active_profile_id()

    if not active_profile_id:
        return None
    
    result = profiles_collection.find_one({'_id': ObjectId(active_profile_id)}) or {}

    # Get sessions for profile id
    sessions = get_sessions(active_profile_id)

    result['sessions'] = sessions

    return transform_objectids_to_string(result) or {}

    
    


    