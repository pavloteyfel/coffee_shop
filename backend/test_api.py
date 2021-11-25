from src.database.models import Drink, db
from src.auth.auth import AuthError
from flask_testing import TestCase
from unittest.mock import patch
from functools import wraps
from src.auth import auth

import unittest
import pathlib
import os


# Mock auth wrapper for testing app endpoint without authentication
def mock_requires_auth(permission):
    """Mock authentication function for testing"""
    def requires_auth_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return requires_auth_decorator

# Replace the real authentication decorator with mock function
patch('src.auth.auth.requires_auth', mock_requires_auth).start()

# App must be imported after we mocked the authentication function
from src.api import app


class TestAuthModule(unittest.TestCase):
    def setUp(self):
        self.domain = auth.AUTH0_DOMAIN
        self.well_nown = auth.AUTH0_WELL_KNOWN
        self.algorithms = auth.ALGORITHMS
        self.audience = auth.API_AUDIENCE

    def test_get_jwks(self):
        response = auth.get_jwks(self.well_nown)
        self.assertTrue(response.get('keys'))

    def test_get_token_auth_header(self):
        request = {'Authorization': 'Bearer <TOKEN>'}
        token = auth.get_token_auth_header(request)
        self.assertEqual(token, '<TOKEN>')

    def test_get_token_auth_header_no_header_error(self):
        request = {}
        with self.assertRaises(AuthError) as context:
            auth.get_token_auth_header(request)
        self.assertTrue(context.exception.status_code, 401)
        self.assertTrue(context.exception.error.get('code'), 'no_auth_header')
    
    def test_check_permissions(self):
        payload = {'permissions': ['get:drinks']}
        self.assertTrue(auth.check_permissions('get:drinks', payload))

    def test_check_permissions_400(self):
        payload = {}
        with self.assertRaises(AuthError) as context:
            auth.check_permissions('get:drinks', payload)
        self.assertTrue(context.exception.status_code, 400)

    def test_check_permissions_403(self):
        payload = {'permissions': ['post:drinks']}
        with self.assertRaises(AuthError) as context:
            auth.check_permissions('get:drinks', payload)
        self.assertTrue(context.exception.status_code, 403)


class TestCoffeShopApp(TestCase):

    def create_app(self):
        database_filename = pathlib.Path('src/database/test_database.db')
        project_dir = os.path.dirname(os.path.abspath(__file__))
        database_path = "sqlite:///{}".format(
            os.path.join(project_dir, database_filename))
        app.config['SQLALCHEMY_DATABASE_URI'] = database_path
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()
        drinks = [
            {'title': 'Blue Water',
             'recipe': '[{"name": "water", "color": "blue", "parts": 1}]'}]
        for drink in drinks:
            Drink(**drink).insert()

    def test_get_drinks(self):
        response = self.client.get('/drinks')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(type(data['drinks']), list)

    def test_get_drinks_details(self):
        response = self.client.get('/drinks-detail')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(type(data['drinks']), list)

    def test_post_drinks(self):
        body = {'title': 'Post Drink',
         'recipe': [{'name': 'water', 'color': 'blue', 'parts': 1}]}
        response = self.client.post('/drinks', json=body)
        self.assertEqual(response.status_code, 200)
        drink = Drink.query.filter(Drink.title == 'Post Drink').first()
        self.assertTrue(drink)

    def test_post_drinks_error_409(self):
        body = {'title': 'Post Drink',
         'recipe': [{'name': 'water', 'color': 'blue', 'parts': 1}]}
        response_1 = self.client.post('/drinks', json=body)
        self.assertEqual(response_1.status_code, 200)
        response_2 = self.client.post('/drinks', json=body)
        self.assertEqual(response_2.status_code, 409)

    def test_post_drinks_error_400(self):
        body = {'title': 'Post Drink',
         'recipe': [{'name': 'water', 'color': 'blue'}]}
        response = self.client.post('/drinks', json=body)
        self.assertEqual(response.status_code, 400)

    def test_patch_drinks(self):
        body = {'title': 'Patch Drink'}
        response = self.client.patch('/drinks/1', json=body)
        self.assertEqual(response.status_code, 200)
        drink = Drink.query.get(1)
        self.assertEqual(drink.title, 'Patch Drink')

    def test_patch_drinks_error_404(self):
        body = {'title': 'Patch Drink'}
        response = self.client.patch('/drinks/999', json=body)
        self.assertEqual(response.status_code, 404)

    def test_delete_drinks(self):
        response = self.client.delete('/drinks/1')
        self.assertEqual(response.status_code, 200)
        drink = Drink.query.get(1)
        self.assertFalse(drink)

    def test_delete_drinks_404(self):
        response = self.client.delete('/drinks/999')
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
