from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from flask import request, jsonify

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
        amenity = Amenity(**amenity_data)
        self.amenity_repo.get()
        self.save(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        amenities = Amenity.query.all()
        return [amenity.to_dict() for amenity in amenities]


    def update_amenity(self, amenity_id, amenity_data):
        amenity = Amenity.query.get(amenity_id)
        
        if not amenity:
            return None
        
        amenity.update(amenity_data)

        amenity.save()

        return amenity

    def create_place(self, place_data):
    # Placeholder for logic to create a place, including validation for price, latitude, and longitude
        price = place_data.get("price")
        if price is None or price < 0:
            return jsonify({"error": "Price must be non-negative"}), 400

        owner_id = place_data.get("owner_id")
        if not owner_id:
            return jsonify({"error": "Owner ID is required"}), 400
        
        owner = User.query.get(owner_id)
        if not owner:
            return jsonify({"error": "Owner not found"}), 400


        amenities = place_data.get("amenities")
        if not isinstance(amenities, list):
            return jsonify({"error": "Amenities must be a list of strings"}), 400

        new_place = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=price,
            latitude=place_data.get("latitude"),
            longitude=place_data.get("longitude"),
            owner=owner
        )
        
        new_place.save()
        return new_place


    def get_place(self, place_id):
        # Placeholder for logic to retrieve a place by ID, including associated owner and amenities
        place = Place.query.get(place_id)
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
        places = Place.query.all()
        result = []

        for place in places:
            result.append({
                "id": place.id,
                "title": place.title,
                "latitude": place.latitude,
                "longitude": place.longitude
            })

        return result


    def update_place(self, place_id, place_data):
        # Placeholder for logic to update a place
        place = Place.query.get(place_id)
        if not place:
            return None

        if "title" in place_data:
            place.title = place_data["title"]
        if "description" in place_data:
            place.description = place_data["description"]
        if "price" in place_data:
            place.price = place_data["price"]
        if "latitude" in place_data:
            place.latitude = place_data["latitude"]
        if "longitude" in place_data:
            place.longitude = place_data["longitude"]

        place.save()
        return place

    def create_review(self, review_data):
    # Placeholder for logic to create a review, including validation for user_id, place_id, and rating
        user_id = review_data.get("user_id")
        place_id = review_data.get("place_id")
        text = review_data.get("text")
        rating = review_data.get("rating")

        if not all([user_id, place_id, text, rating]):
            return {"error": "Missing required fields"}, 400

        if not isinstance(rating, int) or not (1 <= rating <= 5):
            return {"error": "Rating must be between 1 and 5"}, 400

        user = self.user_repo.get(user_id)
        if not user:
            return {"error": "User not found"}, 404

        place = self.place_repo.get(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        review = Review(user=user, place=place, text=text, rating=rating)
        self.review_repo.add(review)

        return review.to_dict(), 201

    def get_review(self, review_id):
        # Placeholder for logic to retrieve a review by ID
        review = self.review_repo.get(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review.to_dict(), 200

    def get_all_reviews(self):
        # Placeholder for logic to retrieve all reviews
        reviews = self.review_repo.get_all()
        return [review.to_dict() for review in reviews], 200

    def get_reviews_by_place(self, place_id):
        # Placeholder for logic to retrieve all reviews for a specific place
        reviews = self.review_repo.get_all()
        filtered_reviews = [r for r in reviews if r.place.id == place_id]
        return [r.to_dict() for r in filtered_reviews], 200

    def update_review(self, review_id, review_data):
        # Placeholder for logic to update a review
        review = self.review_repo.get(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        
        if "text" in review_data:
            review.text = review_data["text"]

        if "rating" in review_data:
            rating = review_data["rating"]
            if not isinstance(rating, int) or not (1 <= rating <= 5):
                return {"error": "Rating must be between 1 and 5"}, 400
            review.rating = rating

        review.save()
        return review.to_dict(), 200

    def delete_review(self, review_id):
        # Placeholder for logic to delete a review
        review = self.review_repo.get(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        self.review_repo.delete(review_id)
        return {"message": "Review deleted"}, 200