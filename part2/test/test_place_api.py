import unittest
from app import create_app

class TestPlaceAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

        # Create a user
        self.user_data = {
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice@example.com"
        }
        user_resp = self.client.post('/api/v1/users/', json=self.user_data)
        self.assertEqual(user_resp.status_code, 201)
        self.user_id = user_resp.get_json()["id"]

        # Create an amenity
        amenity_resp = self.client.post('/api/v1/amenities/', json={"name": "Wi-Fi"})
        self.assertEqual(amenity_resp.status_code, 201)
        self.amenity_id = amenity_resp.get_json()["id"]

        # Create a place
        self.place_data = {
            "title": "Nice Place",
            "description": "Comfortable and clean",
            "price": 100,
            "latitude": 45.0,
            "longitude": 1.0,
            "owner_id": self.user_id,
            "amenities": [self.amenity_id]
        }
        place_resp = self.client.post('/places/', json=self.place_data)
        self.assertEqual(place_resp.status_code, 201)
        self.place_id = place_resp.get_json()["id"]

    def test_create_valid_place(self):
        self.assertIsNotNone(self.place_id)

    def test_create_place_missing_title(self):
        data = self.place_data.copy()
        del data["title"]
        resp = self.client.post('/places/', json=data)
        self.assertEqual(resp.status_code, 400)

    def test_create_place_invalid_price(self):
        data = self.place_data.copy()
        data["price"] = -10
        resp = self.client.post('/places/', json=data)
        self.assertEqual(resp.status_code, 400)

    def test_get_all_places(self):
        resp = self.client.get('/places/')
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.get_json(), list)

    def test_get_nonexistent_place(self):
        resp = self.client.get('/places/nonexistent-id')
        self.assertEqual(resp.status_code, 404)

if __name__ == '__main__':
    unittest.main()
