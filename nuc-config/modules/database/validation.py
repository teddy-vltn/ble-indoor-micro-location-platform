from modules.database.database import profiles_collection
from modules.database.utils.profile_utils import create_profile
from modules.database.utils.cache_utils import add_to_cache

def validate_database():
    if not profiles_collection.find_one():
        result = create_profile('default')
        if not result:
            print("Failed to create default profile.")
            exit(1)

        add_to_cache('active_profile', result.inserted_id)