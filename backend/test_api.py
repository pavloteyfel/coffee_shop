from src.database.models import Drink, db
from flask_testing import TestCase
from unittest.mock import patch
from functools import wraps

import unittest
import pathlib
import os

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

class CoffeShopApiTestCase(TestCase):

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


    def test_example(self):
        response = self.client.get('/drinks-detail')
        print(response.get_json())
        # print(response.get_json())

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
