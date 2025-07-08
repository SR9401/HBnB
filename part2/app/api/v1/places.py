from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Entrez 'Bearer ' suivi de votre token JWT"
    }
}

api = Namespace('places', description='Place operations', authorizations=authorizations, security='Bearer Auth')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner details'),
    'amenities': fields.List(fields.String, description="List of amenities IDs")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    @api.doc(security='Bearer Auth')

    def post(self):
        """Register a new place"""
        current_user_id = get_jwt_identity()
        place_data = api.payload
        if not isinstance(place_data, dict):
            return {'error': 'Invalid JSON payload'}, 400

        place_data['owner_id'] = current_user_id

        user = facade.user_repo.get(current_user_id)
        if not user:
            return {'error': 'User not found'}, 404

        try:
            new_place = facade.create_place(place_data)
            return new_place, 201
        except Exception as e:
            return {'error': str(e)}, 400


    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict_list(), 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    @api.doc(security='Bearer Auth')
    
    def put(self, place_id):
        current_user = get_jwt_identity()
        
        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        """Update a place's information"""
        current_user_id = get_jwt_identity()
        place_data = api.payload
        place = facade.get_place(place_id)

        if not place:
            return {'error': 'Place not found'}, 404

        if place.owner.id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        if 'owner_id' in place_data:
            owner = facade.get_user(place_data['owner_id'])
            if not owner:
                return {'error': 'Owner not found'}, 404
            place_data['owner'] = owner
            
        try:
            facade.update_place(place_id, place_data)
            return {'message': 'Place updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400


@api.route('/<place_id>/amenities')
class PlaceAmenities(Resource):
    @api.expect([amenity_model])
    @api.response(200, 'Amenities added successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def post(self, place_id):
        """Add amenities to a place"""
        amenities_data = api.payload
        if not amenities_data:
            return {'error': 'Invalid input data'}, 400

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        for amenity_data in amenities_data:
            amenity = facade.get_amenity(amenity_data['id'])
            if not amenity:
                return {'error': f'Amenity with ID {amenity_data["id"]} not found'}, 404

        for amenity_data in amenities_data:
            place.add_amenity(amenity_data)

        return {'message': 'Amenities added successfully'}, 200

@api.route('/<place_id>/reviews/')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return [review.to_dict() for review in place.reviews], 200
