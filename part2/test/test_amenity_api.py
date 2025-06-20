import unittest
from app import create_app

class TestAmenityAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    def test_create_valid_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={"name": "Wi-Fi"})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["name"], "Wi-Fi")

    def test_create_amenity_missing_name(self):
        response = self.client.post('/api/v1/amenities/', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_create_duplicate_amenity(self):
        self.client.post('/api/v1/amenities/', json={"name": "Parking"})
        response = self.client.post('/api/v1/amenities/', json={"name": "Parking"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("already registered", response.get_json().get("error", ""))

    def test_get_all_amenities(self):
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_nonexistent_amenity(self):
        response = self.client.get('/api/v1/amenities/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_update_amenity(self):
        post_response = self.client.post('/api/v1/amenities/', json={"name": "Old Name"})
        amenity_id = post_response.get_json()["id"]
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={"name": "New Name"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["name"], "New Name")

    def test_update_amenity_missing_name(self):
        post_response = self.client.post('/api/v1/amenities/', json={"name": "ToUpdate"})
        amenity_id = post_response.get_json()["id"]
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={})
        self.assertEqual(response.status_code, 400)

    def test_update_nonexistent_amenity(self):
        response = self.client.put('/api/v1/amenities/nonexistent-id', json={"name": "DoesNotExist"})
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
