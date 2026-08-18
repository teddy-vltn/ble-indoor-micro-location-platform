from flask import request
from flask_restx import Resource, fields

from lib.api import send_error, send_success, create_combined_model
from lib.models import graph_model, error_response, generic_success_response

from modules.database.utils.graphs_utils import update_profile_graph, download_graph_yaml
from modules.database.query.get_active_profile_graph import get_active_profile_graph

from lib.api import api

graph_ns = api.namespace('graph', description='Graph operations')

@graph_ns.route('')
@api.response(400, 'Error updating the graph', model=error_response)
@api.response(200, 'Success', model=generic_success_response)
class Graph(Resource):
    @api.doc(description='Retrieve the graph for the active profile')
    @api.marshal_with(create_combined_model(graph_model), code=200, description='Graph retrieved successfully')
    def get(self):
        """Retrieve the graph for the active profile."""
        try:
            graph = get_active_profile_graph()
            return send_success("Graph retrieved successfully", graph)
        except Exception as e:
            return send_error(str(e))

    @api.expect(graph_model)
    @api.doc(description='Update the graph for the active profile')
    def put(self):
        """Update the graph for the active profile."""
        graph_data = request.json
        updated_graph = update_profile_graph(graph_data)
        if updated_graph.get('error'):
            return send_error(updated_graph.get('error'))
        return send_success("Graph updated successfully", updated_graph)

@graph_ns.route('/download')
@api.response(400, 'Error downloading the graph', model=error_response)
@api.response(200, 'Success', model=generic_success_response)
class GraphDownload(Resource):
    @api.doc(description='Download the graph as a YAML file for the active profile')
    def get(self):
        """Download the graph as a YAML file for the active profile."""
        try:
            return download_graph_yaml()
        except Exception as e:
            return send_error(str(e))
