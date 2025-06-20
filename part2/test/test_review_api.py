import unittest
from app import create_app

class TestReviewAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

        # Création d'un user valide
        user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com"
        }
        response = self.client.post('/api/v1/users/', json=user_data)
        print("Create user status:", response.status_code, response.data)
        self.assertEqual(response.status_code, 201)
        self.user_id = response.get_json()['id']

        # Création d'une place valide
        place_data = {
            "title": "Test Place",
            "description": "A nice place",
            "price": 50.0,
            "latitude": 45.0,
            "longitude": 3.0,
            "owner_id": self.user_id,
            "amenities": []
        }
        response = self.client.post('/api/v1/places/', json=place_data)
        print("Create place status:", response.status_code, response.data)
        self.assertEqual(response.status_code, 201)
        self.place_id = response.get_json()['id']

    def test_create_review(self):
        review_data = {
            "text": "Great place!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        }
        response = self.client.post('/api/v1/reviews/', json=review_data)
        print("Create review status:", response.status_code, response.data)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["text"], "Great place!")
        self.assertEqual(data["rating"], 5)

if __name__ == "__main__":
    unittest.main()
