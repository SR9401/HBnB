from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.models.review import Review

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        reviews = facade.get_reviews_by_place(place_id)
        result = []
        for review in reviews:
            result.append({
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user.id,
                'place_id': review.place.id
            })
        return result, 200

    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self, place_id):
        """Register a new review"""
        review_data = api.payload

        if "user_id" not in review_data:
            return {'error': 'User ID is required'}, 400

        user_id = review_data.get("user_id")
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        try:
            review = Review(
                text=review_data.get("text"),
                rating=review_data.get("rating"),
                place=place,
                user=user
            )
        except (TypeError, ValueError) as e:
            return {'error': str(e)}, 400

        try:
            facade.review_repo.add(review)
        except Exception:
            return {'error': 'Failed to save review'}, 500

        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': user.id,
            'place_id': place.id
        }, 201
