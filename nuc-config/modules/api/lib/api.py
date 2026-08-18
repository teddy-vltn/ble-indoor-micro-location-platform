from flask_restx import Api, fields
from flask import jsonify, make_response

# Initialize the RESTful API with Flask-RESTx
api = Api(version='1.0', title='Game API', description='An API for managing game sessions and player interactions.')

from modules.database.utils.hosts_utils import refresh_hosts_cache
from modules.database.validation import validate_database

validate_database()
refresh_hosts_cache()

# Define utility functions to send responses
def send_error(message, payload=None, code=400):
    """
        Send an error response.

        :param message: The error message to send.
        :param payload: The data to send with the error response.
        :param code: The HTTP status code to return.
        :return: The error response.
    """

    response = {
        "status": "error",
        "message": message,
        "data": payload,
        "code": code
    }
    return response, code

def send_missing_params_error(params):
    """
        Send an error response for missing parameters.

        :param params: The missing parameters.
        :return: The error response.
    """

    return send_error(f"Missing required parameter: {', '.join(params)}", code=400)

def send_not_found_error(message):
    """
        Send a not found error response.

        :param message: The error message to send.
        :return: The not found error response.
    """

    return send_error(message, code=404)

def send_success(message, payload=None, code=200):
    """
        Send a success response.

        :param message: The success message to send.
        :param payload: The data to send with the success response.
        :return: The success response.
    """

    response = {
        "status": "success",
        "message": message,
        "data": payload,
        "code": code
    }
    return response, code

def create_combined_model(data_model):
    """
        Create a combined model for a successful response.

        :param data_model: The model to use for the response data.
        :return: The combined model for the response.
    """

    return api.model(f'{data_model.name}SuccessResponse', {
        "message": fields.String(description="Success message", example="Data retrieved successfully"),
        "status": fields.String(description="Status of the response", example="success"),
        "data": fields.Nested(data_model, description="Response data"),
        "code": fields.Integer(description="HTTP status code", example=200)
    })



