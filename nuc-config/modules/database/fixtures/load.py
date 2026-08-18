import json
from pymongo import MongoClient
from bson import ObjectId

# Get where the file executes
def get_base_path():
    import os
    return os.path.dirname(os.path.abspath(__file__))

data_path = get_base_path() + '/data/'

def convert_oid_fields(data):
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            if key == '$oid':
                return ObjectId(value)
            elif isinstance(value, dict):
                new_data[key] = convert_oid_fields(value)
            elif isinstance(value, list):
                new_data[key] = [convert_oid_fields(item) for item in value]
            else:
                new_data[key] = value
        return new_data
    elif isinstance(data, list):
        return [convert_oid_fields(item) for item in data]
    return data

# Incase it's the wrong type of export that is selected in mongo express
def transform_multiroot_json(input_file):
    data_list = []
    with open(input_file, 'r') as infile:
        for line in infile:
            data_list.append(json.loads(line.strip()))
    return data_list

def load_json(filename):
    with open(data_path + filename, 'r') as file:
        print(f'Loading {filename}...')
        try:
            data = json.load(file)
            return data
        except json.JSONDecodeError:
            print('Transforming multiroot JSON...')
            data = transform_multiroot_json(data_path + filename)
            return data

def import_to_mongodb(collection, data):
    data = convert_oid_fields(data)

    if isinstance(data, list):
        collection.insert_many(data)
    else:
        collection.insert_one(data)

def main():
    # MongoDB connection setup
    client = MongoClient("mongodb://127.0.0.1:27017/")

    # Initialize the database
    db = client["test"]

    # drop all collections
    db.cache.drop()
    db.graphs.drop()
    db.groups.drop()
    db.hosts.drop()
    db.profiles.drop()
    db.script_logs.drop()
    db.sessions.drop()
    db.players.drop()

    # List of JSON files to import
    files = {
        'cache': 'cache.json',
        'graphs': 'graphs.json',
        'groups': 'groups.json',
        'hosts': 'hosts.json',
        'profiles': 'profiles.json',
        'script_logs': 'script_logs.json',
        'sessions': 'sessions.json',
        'players': 'players.json'
    }

    for collection_name, filename in files.items():
        data = load_json(filename)
        collection = db[collection_name]
        import_to_mongodb(collection, data)
        print(f'Imported {filename} into {collection_name} collection.')

if __name__ == '__main__':
    main()
