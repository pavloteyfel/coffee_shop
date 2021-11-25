from flask import Flask, jsonify, abort, g as payload, make_response
from .auth.auth import AuthError, requires_auth
from .database.models import setup_db, Drink, db_drop_and_create_all
from flask_expects_json import expects_json
from jsonschema import ValidationError
from flask_cors import CORS

import pathlib
import json
import os


app = Flask(__name__)
SECRET_KEY = os.urandom(32)
setup_db(app)
CORS(app)

# Creates database with seed data if it not exists
if not pathlib.Path('database/database.db').exists():
    db_drop_and_create_all()

# --------------------------------------------------------------------------- #
# Validation schemas for payloads based on https://json-schema.org
# --------------------------------------------------------------------------- #

create_drinks_schema = {
    'type': 'object',
    'properties': {
        'title': {'type': 'string'},
        'recipe': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'color': {'type': 'string'},
                    'parts': {'type': 'number'}
                },
                'required': ['name', 'color', 'parts']
            }
        },
    },
    'required': ['title', 'recipe']
}

update_drinks_schema = {
    'type': 'object',
    'anyOf': [
        {
            'properties': {
                'title': {'type': 'string'},
            },
            'required': ['title']
        },
        {
            'properties': {
                'recipe': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'name': {'type': 'string'},
                            'color': {'type': 'string'},
                            'parts': {'type': 'number'}
                        },
                        'required': ['name', 'color', 'parts']
                    }
                },
            },
            'required': ['recipe']
        }
    ],
}


# --------------------------------------------------------------------------- #
# Routes
# --------------------------------------------------------------------------- #

@app.route('/drinks')
def get_drinks():
    '''
    A public endpoint, contains only the drink.short() data representation.

    Returns:
        - status code 200 and json {"drinks": drinks} where drinks is the
    list of drinks or appropriate status code indicating reason for failure.
    '''
    drinks = Drink.query.all()

    # 404 if there are no drinks entries
    if not drinks:
        abort(404)

    return jsonify({
        'drinks': [drink.short() for drink in drinks],
    }), 200


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail():
    '''
    Shows the drink's details

    - Requires the 'get:drinks-detail' permission
    - Contains the drink.long() data representation

    Returns:
        - status code 200 and json {"drinks": drinks} where drinks is the
    list of drinks or appropriate status code indicating reason for failure
    '''
    drinks = Drink.query.all()

    # 404 if there are no drinks entries
    if not drinks:
        abort(404)

    return jsonify({
        'drinks': [drink.long() for drink in drinks],
    }), 200


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
@expects_json(create_drinks_schema)
def create_drinks():
    '''
    - Creates a new row in the drinks table
    - Requires the 'post:drinks' permission

    Returns:
        - status code 200 and json {"drinks": drink}, where drink an array
    containing only the newly created drink or appropriate status code
    indicating reason for failure
    '''

    drink = Drink.query.filter(
        Drink.title == payload.data.get('title')).first()

    # 409 posted drink already exists
    # https://stackoverflow.com/questions/12658574/rest-api-design-post-to-create-with-duplicate-data-would-be-integrityerror-500
    if drink:
        abort(409)

    drink = Drink(
        title=payload.data.get('title'),
        recipe=json.dumps(payload.data.get('recipe'))
    )

    # Save drink data
    drink_data = drink.long()

    # Throws 422 if there are problems during database transaction
    # Retrieve id of the new drink
    drink_id = drink.insert()

    # Propagate back the id
    drink_data['id'] = drink_id

    return jsonify({
        'drinks': [drink_data]
    }), 200


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
@expects_json(update_drinks_schema)
def update_drinks(id):
    '''
    Arguments:
        - <id> is the existing model id

    - Responds with a 404 error if <id> is not found
    - Updates the corresponding row for <id>
    - Requires the 'patch:drinks' permission
    - Contains the drink.long() data representation

    Returns:
        - status code 200 and json {"drinks": drink} where drink an array
    containing only the updated drink or appropriate status code indicating
    reason for failure
    '''
    # 404 if no entry found
    drink = Drink.query.get_or_404(id)

    # Updates title property if message contains "title"
    if 'title' in payload.data:
        drink.title = payload.data.get('title')

    # Updates recipe property if message contains "recipe"
    if 'recipe' in payload.data:
        drink.recipe = json.dumps(payload.data.get('recipe'))

    # Detach drink data from the session
    drink_data = drink.long()

    # Throws 422 if there are problems during database transaction
    drink.update()

    return jsonify({
        'drinks': [drink_data]
    }), 200


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(id):
    '''
    Arguments:
        - <id>: is the existing model id

    - Responds with a 404 error if <id> is not found
    - Deletes the corresponding row for <id>
    - Requires the 'delete:drinks' permission
    - Returns status code 200 and json {"delete": id} where id is the id of
    the deleted record or appropriate status code indicating reason for 
    failure
    '''
    # 404 if no entry found
    drink = Drink.query.get_or_404(id)

    # Throws 422 if there are problems during database transaction
    drink.delete()

    return jsonify({
        'delete': id
    }), 200

# --------------------------------------------------------------------------- #
# Error handling
# --------------------------------------------------------------------------- #


@app.errorhandler(400)
def bad_request(error):
    """
    In case of JSON schema Validation error, we provide a detailed
    problem description about the received message.
    """
    if isinstance(error.description, ValidationError):
        original_error = error.description
        return make_response(jsonify({
            'error': 400, 'message': original_error.message
        }), 400)
    return jsonify({'error': 400, 'message': 'bad request'}), 400


@app.errorhandler(AuthError)
def auth_error(error):
    """Used for authentication/authorization errors"""
    status_code = error.status_code
    description = error.error.get('description')
    return jsonify({
        'error': status_code, 'message': description
    }), status_code


@app.errorhandler(401)
def unathorized(error):
    return jsonify({'error': 401, 'message': 'unathorized'}), 401


@app.errorhandler(403)
def forbidden(error):
    return jsonify({'error': 403, 'message': 'forbidden'}), 403


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({'error': 404, 'message': 'resource not found'}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 405, 'message': 'method not allowed'}), 405


@app.errorhandler(409)
def conflict(error):
    return jsonify({'error': 409, 'message': 'resource already exists'}), 409


@app.errorhandler(422)
def unprocessable_entity(error):
    return jsonify({'error': 422, 'message': 'unprocessable entity'}), 422
