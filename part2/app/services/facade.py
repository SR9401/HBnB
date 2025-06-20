from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # USER
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    # AMENITY
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return [a.to_dict() for a in self.amenity_repo.get_all()]

    def update_amenity(self, amenity_id, data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        amenity.update(data)
        self.amenity_repo.save(amenity)
        return amenity

    # PLACE
    def create_place(self, place_data):
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return [p.to_dict() for p in self.place_repo.get_all()]

    def update_place(self, place_id, data):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        for key in ["title", "description", "price", "latitude", "longitude"]:
            if key in data:
                setattr(place, key, data[key])
        self.place_repo.save(place)
        return place

    # REVIEW
    def create_review(self, review_data):
        user = self.user_repo.get(review_data.get("user_id"))
        place = self.place_repo.get(review_data.get("place_id"))
        rating = review_data.get("rating")

        if not all([user, place, rating, review_data.get("text")]):
            return {"error": "Missing required fields"}, 400
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            return {"error": "Rating must be between 1 and 5"}, 400

        review = Review(user=user, place=place, text=review_data["text"], rating=rating)
        self.review_repo.add(review)
        return review.to_dict(), 201

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        return ({"error": "Review not found"}, 404) if not review else (review.to_dict(), 200)

    def get_all_reviews(self):
        return [r.to_dict() for r in self.review_repo.get_all()], 200

    def get_reviews_by_place(self, place_id):
        return [r.to_dict() for r in self.review_repo.get_all() if r.place.id == place_id], 200

    def update_review(self, review_id, data):
        review = self.review_repo.get(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        if "text" in data:
            review.text = data["text"]
        if "rating" in data:
            rating = data["rating"]
            if not isinstance(rating, int) or not (1 <= rating <= 5):
                return {"error": "Rating must be between 1 and 5"}, 400
            review.rating = rating

        review.save()
        return review.to_dict(), 200

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        self.review_repo.delete(review_id)
        return {"message": "Review deleted successfully"}, 200
