from flask_restx import fields, Model
from lib.api import api

# Models for session management
session_model_create = Model('CreatePlayer', {
    'id_minor': fields.Integer(required=True, description='The minor ID'),
    'devices': fields.List(fields.String, description='List of device IDs associated with the player', example=['device1', 'device2'])
})

has_visited_model = Model('HasVisited', {
    'nodes': fields.List(fields.String, required=True, description='List of places that player should have visited', example=['1', '3'])
})

group_host_model = Model('GroupHost', {
    'name': fields.String(required=True, description='Host name in the DNS', example='rasp13.local'),
    'active': fields.Boolean(default=True, description='Whether the host is active to be used in the inventory', example=True),
    'node': fields.String(description='Node associated with the host in Graph Positioning', example='1'),
})

inventory_model = Model('Inventory', {
    'hosts': fields.List(fields.Nested(group_host_model), description='List of hosts in the inventory')
})

# Models for inventory management
group_model = Model('Group', {
    'name': fields.String(required=True, description='The name of the group'),
    #'children': fields.List(fields.String, description='List of child group names'),
    'hosts': fields.List(fields.Nested(group_host_model), description='List of hosts in the group'),
    #'vars': fields.Raw(description='Variables associated with the group')
})

node_model = api.model('Node', {
    'id': fields.String(required=True, description='Node ID'),
    'name': fields.String(required=True, description='Node name'),
    'x': fields.Float(required=True, description='X coordinate of the node for the dashboard display'),
    'y': fields.Float(required=True, description='Y coordinate of the node for the dashboard display'),
})

edge_model = api.model('Edge', {
    'from': fields.String(required=True, description='Source node ID'),
    'to': fields.String(required=True, description='Target node ID')
})

graph_model = api.model('Graph', {
    'nodes': fields.List(fields.Nested(node_model), required=True, description='List of nodes in the graph'),
    'edges': fields.List(fields.Nested(edge_model), required=True, description='List of edges in the graph')
})

player_model = api.model("Player", {
    "_id": fields.String(description="ID of the player"),
    "id_player": fields.Integer(required=True, description="ID of the user"),
    "id_minor": fields.Integer(required=True, description="ID of the BLE device minor associated for the player"),
    "devices": fields.List(fields.String, description="List of device IDs associated with the player"),
    "session_id": fields.String(description="ID of the session"),
    "started_at": fields.Float(description="Timestamp when the player started"),
    "updated_at": fields.Float(description="Timestamp when the player was last updated"),
    "has_visited": fields.List(fields.String, description="List of nodes that the player has visited", example=["1", "3"]),
    "temporal_sequence_visited": fields.Raw(description="Temporal sequence of nodes visited"),
    "has_finished": fields.Boolean(description="Whether the player has finished the session")
})

session_model = api.model("Session", {
    "_id": fields.String(description="ID of the session"),
    "name": fields.String(required=True, description="Name of the session", example="Matin"),
    "profile_id": fields.String(required=True, description="ID of the profile"),
    "started_at": fields.Float(description="Timestamp when the session started", example=1630000000.0),
    "finished_at": fields.Float(description="Timestamp when the session was finished", example=1680000000.0),
    "players": fields.List(fields.Nested(player_model), description="List of players in the session"),
})

profile_model = api.model('Profile', {
    '_id': fields.String(description='ID of the profile'),
    'name': fields.String(required=True, description='Name of the profile', example='Fête de la Science 2024'),
    'created_at': fields.Float(description='Timestamp when the profile was created'),
    'updated_at': fields.Float(description='Timestamp when the profile was last updated'),
    'graph_id': fields.String(required=True, description='ID of the graph associated with the profile'),
    'group_id': fields.String(required=True, description='ID of the group associated with the profile'),
    'graph_svg': fields.String(required=True, description='Graph SVG file name', example='map.svg'),
    'sessions': fields.List(fields.Nested(session_model), description='List of session IDs associated with the profile')
})

host_cache_model = api.model("HostCache", {
    "name": fields.String(description="Host name in DNS", example="rasp13.local"),
    "active": fields.Boolean(description="Whether the host is active", example=True),
    "node": fields.String(description="Node associated with the host in Graph Positioning", example="1"),
    "online": fields.Boolean(description="Whether the host is online on the network.", example=True),
    "services": fields.Raw(description="State of services running on the host, Boolean for running or not and None|null for uncertain", example={ "rasplogs": False, "filebeat": True }),
    "last_pings": fields.List(fields.Boolean, description="List of last pings", example=[True, False, True]),
    "timestamp_last_successful_ping": fields.Float(description="Timestamp of the last successful ping")
})

generic_success_response = api.model("GenericSuccessResponse", {
    "message": fields.String(description="Success message", example="The operation was a success"),
    "status": fields.String(description="Status of the response", example="success"),
    "data": fields.Raw(description="Response data"),
    "code": fields.Integer(description="HTTP status code", example=200)
})

error_response = api.model("ErrorResponse", {
    "message": fields.String(description="Error message", example="The operation failed"),
    "status": fields.String(description="Status of the response", example="error"),
    "data": fields.Raw(description="Response data"),
    "code": fields.Integer(description="HTTP status code", example=400)
})

not_found_error_response = api.model("NotFoundErrorResponse", {
    "message": fields.String(description="Error message", example="The resource was not found"),
    "status": fields.String(description="Status of the response", example="error"),
    "data": fields.Raw(description="Response data"),
    "code": fields.Integer(description="HTTP status code", example=404)
})

# Add models to the API
api.add_model(session_model_create.name, session_model_create)
api.add_model(has_visited_model.name, has_visited_model)
api.add_model(group_host_model.name, group_host_model)
api.add_model(inventory_model.name, inventory_model)
api.add_model(group_model.name, group_model)
api.add_model(node_model.name, node_model)
api.add_model(edge_model.name, edge_model)
api.add_model(graph_model.name, graph_model)
api.add_model(player_model.name, player_model)
api.add_model(session_model.name, session_model)
api.add_model(generic_success_response.name, generic_success_response)
api.add_model(error_response.name, error_response)

