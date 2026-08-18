from bson.objectid import ObjectId
from modules.database.database import groups_collection, hosts_collection

def create_group():
    return groups_collection.insert_one({'hosts': []})

def delete_group(group_id):
    """Delete the group with the specified ID."""
    # Fetch the group to be deleted
    group = groups_collection.find_one({'_id': ObjectId(group_id)})
    if not group:
        return False

    # Delete each host
    for host_id in group['hosts']:
        hosts_collection.delete_one({'_id': ObjectId(host_id)})

    # Delete the group
    groups_collection.delete_one({'_id': ObjectId(group_id)})

    return True

def duplicate_group(group_id):
    """Duplicate the group with the specified ID."""
    # Fetch the group to be duplicated
    group = groups_collection.find_one({'_id': ObjectId(group_id)})
    if not group:
        return None

    # Duplicate each host
    new_host_ids = []
    for host_id in group['hosts']:
        host = hosts_collection.find_one({'_id': ObjectId(host_id)})
        if host:
            # Remove the _id field to create a new host document
            host.pop('_id', None)
            new_host_id = hosts_collection.insert_one(host).inserted_id
            new_host_ids.append(new_host_id)

    # Create a new group with the duplicated hosts
    new_group_data = {
        'hosts': new_host_ids,
    }

    # Insert the new group document
    new_group = groups_collection.insert_one(new_group_data)

    return new_group


