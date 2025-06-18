from app.persistence.repository import InMemoryRepository
from flask import jsonify
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    def create_amenity(self, amenity_data):
    # Placeholder for logic to create an amenity
        pass

    def get_amenity(self, amenity_id):
    # Placeholder for logic to retrieve an amenity by ID
     pass

    def get_all_amenities(self):
    # Placeholder for logic to retrieve all amenities
        pass

    def update_amenity(self, amenity_id, amenity_data):
    # Placeholder for logic to update an amenity
        pass

    def create_place(self, place_data):
    # Placeholder for logic to create a place, including validation for price, latitude, and longitude
        price = place_data.get("price")
        if price is None or price < 0:
            return jsonify({"error": "Price must be non-negative"}), 400

        owner_id = place_data.get("owner_id")
        if not owner_id:
            return jsonify({"error": "Owner ID is required"}), 400

        amenities = place_data.get("amenities")
        if not isinstance(amenities, list):
            return jsonify({"error": "Amenities must be a list of strings"}), 400

        new_place = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=price,
            latitude=place_data.get("latitude"),
            longitude=place_data.get("longitude"),
            owner_id=owner_id
        )
        
        new_place.save()
        return new_place


    def get_place(self, place_id):
        # Placeholder for logic to retrieve a place by ID, including associated owner and amenities
        place = place_id.get("place_id")
        if not place:
            return None
        owner = place.owner
        amenities = place.amenities
        return {
        "id": place.id,
        "title": place.title,
        "description": place.description,
        "latitude": place.latitude,
        "longitude": place.longitude,
        "owner": {
            "id": owner.id,
            "first_name": owner.first_name,
            "last_name": owner.last_name,
            "email": owner.email
        },
        "amenities": [
            {"id": a.id, "name": a.name} for a in amenities
        ]
    }

    def get_all_places(self):
        # Placeholder for logic to retrieve all places
        pass

    def update_place(self, place_id, place_data):
        # Placeholder for logic to update a place
        pass

    def create_review(self, review_data):
    # Placeholder for logic to create a review, including validation for user_id, place_id, and rating
        pass

    def get_review(self, review_id):
        # Placeholder for logic to retrieve a review by ID
        pass

    def get_all_reviews(self):
        # Placeholder for logic to retrieve all reviews
        pass

    def get_reviews_by_place(self, place_id):
        # Placeholder for logic to retrieve all reviews for a specific place
        pass

    def update_review(self, review_id, review_data):
        # Placeholder for logic to update a review
        pass

    def delete_review(self, review_id):
        # Placeholder for logic to delete a review
        pass