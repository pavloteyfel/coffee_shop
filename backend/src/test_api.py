import unittest
from flask_testing import TestCase

import unittest
import logging

# Turning off migration related logging INFO
logging.getLogger('alembic.runtime.migration').disabled = True

class CoffeShopApiTestCase(TestCase):
    pass

if __name__ == '__main__':
    unittest.main()