from pymongo import MongoClient
import bson
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

all_collections = []

# Initialize MongoDB client using environment variables
client = MongoClient(os.getenv('MONGODB_URI'))

# Initialize the database
db = client[os.getenv('MONGODB_DATABASE')]

def create_collection(collection_name):
    """Create a new collection."""
    collection = db[collection_name]
    all_collections.append(collection)
    return collection

# Initialize the cache collection
cache_collection = create_collection('cache')

# Initialize the graph collection
graphs_collection = create_collection('graphs')

# Initialize the group collection
groups_collection = create_collection('groups')

# Initialize the host collection
hosts_collection = create_collection('hosts')

# Initialize the player collection
players_collection = create_collection('players')

# Profile collection: data about the profiles
profiles_collection = create_collection('profiles')

# Session collection: data about the sessions
sessions_collection = create_collection('sessions')

# Logs collection: data from logstash
logs_collection = db[os.getenv('LOGSTASH_LOGS_COLLECTION')]

# Active profile key in cache
active_profile_key = 'active_profile'

# Session key in cache
active_session_key = 'active_session'

# Ansible vars key in cache
ansible_vars_key = 'ansible_config'

# Transforms keys objectids to strings
def transform_objectids_to_string(obj):
    if type(obj) == bson.objectid.ObjectId:
        return str(obj)
    
    if type(obj) != dict:
        return obj
    
    for key in obj.keys():
        if type(obj[key]) == list:
            obj[key] = [transform_objectids_to_string(item) for item in obj[key]]
        if type(obj[key]) == dict:
            obj[key] = transform_objectids_to_string(obj[key])
        if type(obj[key]) == bson.objectid.ObjectId:
            obj[key] = str(obj[key])

    return obj
