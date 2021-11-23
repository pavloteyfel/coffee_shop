from src.database.models import Drink, db
from flask_testing import TestCase
from src.api import app

import unittest
import pathlib
import os

# Turning off migration related logging INFO
# logging.getLogger('alembic.runtime.migration').disabled = True
# Mocking jwt_decode_handler:
# https://stackoverflow.com/questions/55597216/authenticate-flask-unit-test-client-from-another-service-microservices-architec
# python -m unittest -v

class CoffeShopApiTestCase(TestCase):

    def create_app(self):
        database_filename = pathlib.Path('src/database/test_database.db')
        project_dir = os.path.dirname(os.path.abspath(__file__))
        database_path = "sqlite:///{}".format(
            os.path.join(project_dir, database_filename))
        app.config['SQLALCHEMY_DATABASE_URI'] = database_path
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(app)
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()
        drinks = [
            {'title': 'Water',
             'recipe': '[{"name": "water", "color": "blue", "parts": 1}]'}]
        for drink in drinks:
            Drink(**drink).insert()

    def test_example(self):
        pass

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
