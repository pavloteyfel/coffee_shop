import unittest
from src.auth.auth import AuthError
from src.auth import auth

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


if __name__ == '__main__':
    unittest.main()