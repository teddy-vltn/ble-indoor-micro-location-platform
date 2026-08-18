from bson import ObjectId
from modules.database.database import profiles_collection, transform_objectids_to_string

def get_all_profiles():
    """Retrieve all profiles with the count of graph nodes, group hosts, and player count."""
    pipeline = [
        {
            '$lookup': {
                'from': 'graphs',  # Collection name for graphs
                'localField': 'graph_id',
                'foreignField': '_id',
                'as': 'graph'
            }
        },
        {
            '$lookup': {
                'from': 'groups',  # Collection name for groups
                'localField': 'group_id',
                'foreignField': '_id',
                'as': 'group'
            }
        },
        {
            '$lookup': {
                'from': 'players',  # Collection name for players
                'localField': '_id',
                'foreignField': 'profile_id',
                'as': 'players'
            }
        },
        {
            '$unwind': {
                'path': '$graph',
                'preserveNullAndEmptyArrays': True
            }
        },
        {
            '$unwind': {
                'path': '$group',
                'preserveNullAndEmptyArrays': True
            }
        },
        {
            '$addFields': {
                'player_count': {'$size': '$players'},
                'graph_node_count': {'$size': '$graph.nodes'},
                'group_host_count': {'$size': '$group.hosts'}
            }
        },
        {
            '$project': {
                '_id': 1,
                'name': 1,
                'graph_svg': 1,
                'sessions': 1,
                'created_at': 1,
                'updated_at': 1,
                'graph_node_count': 1,
                'group_host_count': 1,
                'player_count': 1
            }
        }
    ]

    result = list(profiles_collection.aggregate(pipeline))

    for profile in result:
        profile = transform_objectids_to_string(profile)

    return result