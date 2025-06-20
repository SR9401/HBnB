import unittest
from app import create_app

class TestUserAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    def test_create_valid_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice@example.com"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["email"], "alice@example.com")

    def test_create_user_invalid_email(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Bob",
            "last_name": "Brown",
            "email": "bobemail.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_empty_fields(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": ""
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_long_first_name(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "A" * 51,
            "last_name": "Doe",
            "email": "longname@example.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_duplicate_email(self):
        self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "duplicate@example.com"
        })
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "duplicate@example.com"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Email already registered", response.get_json().get("error", ""))

    def test_get_all_users(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_nonexistent_user(self):
        response = self.client.get('/api/v1/users/nonexistent-id')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
