from .database.models import db_drop_and_create_all, setup_db, Drink, db
from flask import Flask, request, jsonify, abort, g as payload, make_response
from .auth.auth import AuthError, requires_auth
from flask_expects_json import expects_json
from jsonschema import ValidationError
from flask_cors import CORS
from sqlalchemy import exc

import json
import os


app = Flask(__name__)
setup_db(app)
CORS(app)


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
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where 
    drinks is the list of drinks
        or appropriate status code indicating reason for failure
    '''
    drinks = Drink.query.all()

    # 404 if there are no drinks entries
    if not drinks:
        abort(404)

    return jsonify({
        'drinks': [drink.short() for drink in drinks],
    }), 200

@app.route('/drinks-detail')
def get_drinks_detail():
    '''
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where 
    drinks is the list of drinks
        or appropriate status code indicating reason for failure
    '''
    drinks = Drink.query.all()

    # 404 if there are no drinks entries
    if not drinks:
        abort(404)

    return jsonify({
        'drinks': [drink.long() for drink in drinks],
    }), 200

@app.route('/drinks', methods=['POST'])
@expects_json(create_drinks_schema)
def create_drinks():
    '''
        POST /drinks
            it should create a new row in the drinks table
            it should require the 'post:drinks' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink} 
        where drink an array containing only the newly created drink
            or appropriate status code indicating reason for failure
    '''

    drink = Drink.query.filter(
        Drink.title == payload.data.get('title')).first()
    
    # 409 https://stackoverflow.com/questions/12658574/rest-api-design-post-to-create-with-duplicate-data-would-be-integrityerror-500
    if drink:
        abort(409)

    drink = Drink(
        title = payload.data.get('title'),
        recipe = json.dumps(payload.data.get('recipe'))
    )

    # Detach drink data from the session
    drink_data = drink.long()

    # Throws 422 if there are problems during database transaction
    drink.insert()

    return jsonify({
        'drinks': [drink_data]
    }), 200

@app.route('/drinks/<int:id>', methods=['PATCH'])
@expects_json(update_drinks_schema)
def update_drinks(id):
    '''
        PATCH /drinks/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:drinks' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink} 
        where drink an array containing only the updated drink
            or appropriate status code indicating reason for failure
    '''
    # 404 if no entry found
    drink = Drink.query.get_or_404(id)

    # Updates title property if message contains "title"
    if 'title' in  payload.data:
        drink.title = payload.data.get('title')

    # Updates recipe property if message contains "recipe"
    if 'recipe' in  payload.data:
        drink.recipe = json.dumps(payload.data.get('recipe'))
    
    # Detach drink data from the session
    drink_data = drink.long()

    # Throws 422 if there are problems during database transaction
    drink.update()

    return jsonify({
        'drinks': [drink_data]
    }), 200

@app.route('/drinks/<int:id>', methods=['DELETE'])
def delete_drinks(id):
    '''
        DELETE /drinks/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:drinks' permission
        returns status code 200 and json {"success": True, "delete": id} where 
        id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''
    # 404 if no entry found
    drink = Drink.query.get_or_404(id)

    # Throws 422 if there are problems during database transaction
    drink.delete()

    return jsonify({
        'detele': id
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
        return make_response(
            jsonify(
                {'error': 400, 'message': original_error.message}), 400)
    return jsonify({'error': 400, 'message': 'bad request'}), 400

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

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''

if __name__ == "__main__":
    app.debug = True
    app.run()
