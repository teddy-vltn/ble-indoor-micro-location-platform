from modules.database.database import graphs_collection
from bson import ObjectId
from modules.database.query.get_active_profile_graph import get_active_profile_graph
from flask import Response
import yaml

def yaml_download(data, filename="data.yml"):
    """Download data as a YAML file.

    Args:
        data (dict): The data to be downloaded.
        filename (str, optional): The name of the downloaded file. Defaults to "data.yml".

    Returns:
        Response: The response containing the downloaded data as a YAML file.

    """
    # Convert the data to YAML format
    response = yaml.dump(data)

    # Create a Flask response object with the YAML data
    response = Response(response, status=200, mimetype="application/x-yaml")

    # Set the Content-Disposition header to specify the filename for the downloaded file
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"

    return response

def create_graph():
    """Create a new graph with an empty list of nodes and edges."""
    return graphs_collection.insert_one({'nodes': [], 'edges': []})

def delete_graph(graph_id):
    """
    Delete the graph with the specified ID.

    Args:
        graph_id (str): The ID of the graph to be deleted.

    Returns:
        bool: True if the graph is deleted successfully, False otherwise.
    """
    # Delete the graph from the graphs collection using its ID
    # The delete_one method returns a DeleteResult object
    result = graphs_collection.delete_one({'_id': ObjectId(graph_id)})

    # Check if the graph was successfully deleted
    # The deleted_count attribute of the DeleteResult object indicates the number of documents deleted
    # We return True if the deleted_count is greater than 0, indicating that the graph was deleted
    return result.deleted_count > 0

def duplicate_graph(graph_id):
    """
    Duplicate the graph with the specified ID.

    Args:
        graph_id (str): The ID of the graph to be duplicated.

    Returns:
        pymongo.results.InsertOneResult: The result of the insert operation,
        containing the ID of the newly created graph.
    """
    # Find the graph to be duplicated
    result = graphs_collection.find_one({'_id': graph_id})

    # If the graph is not found, return None
    if not result:
        return None

    # Create a new graph with the same nodes and edges as the original graph
    new_graph = graphs_collection.insert_one({
        'nodes': result['nodes'],
        'edges': result['edges']
    })

    # If the insertion operation fails, return None
    if not new_graph:
        return None

    # Return the result of the insert operation, containing the ID of the new graph
    return new_graph

# Function to update the active graph
def update_profile_graph(graph_data):
    """
    Update the graph data for the active profile.

    Args:
        graph_data (dict): The updated graph data.

    Returns:
        dict: The updated graph data or an error message if the profile does not have a graph or the graph is not found.
    """
    # Extract the nodes and edges from the graph data
    nodes = graph_data.get('nodes')
    edges = graph_data.get('edges')

    # Get the active profile's graph
    graph = get_active_profile_graph()
    
    # If the profile does not have a graph, return an error message
    if not graph:
        return {'error': 'Le profil actif n\'a pas de graph', 'code': 404}

    # Update the graph with the new nodes and edges
    result = graphs_collection.update_one(
        {'_id': ObjectId(graph['_id'])},  # Update the graph with the matching ID
        {'$set': {'nodes': nodes, 'edges': edges}}  # Set the new nodes and edges
    )

    # If the graph is not found, return an error message
    if result.matched_count == 0:
        return {'error': 'Graph non trouvé', 'code': 404}

    # Return the updated graph data
    return graph_data

# Function to download the active graph as YAML
def download_graph_yaml(): 
    """
    Download the active graph as a YAML file.

    Returns:
        dict or str: The downloaded graph data or an error message.
    """
    try:
        # Get the ID of the active graph
        id = get_active_profile_graph()
    except ValueError as e:
        # If there's an error, return an error message
        return {'error': str(e), 'code': 400}

    # Find the graph in the database
    graph = graphs_collection.find_one({"_id": id}, {'_id': 0, 'nodes': 1, 'edges': 1})
    
    # If the graph is not found, return an error message
    if not graph:
        return {'error': 'Graph non trouvé', 'code': 404}
    
    # Download the graph as a YAML file
    return yaml_download(graph, filename=f"graph.yml")
