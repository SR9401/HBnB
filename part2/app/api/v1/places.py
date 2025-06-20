from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from app.services.facade import HBnBFacade
from app.models.place import Place

api = Namespace('places', description='Place operations')

# Models
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

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        try:
            data = request.get_json()

            if not data.get("title"):
                return jsonify({"error": "Title is required"}), 400
            if not data.get("description"):
                return jsonify({"error": "Description is missing"}), 400

            price = data.get("price")
            if not isinstance(price, (int, float)) or price < 0:
                return jsonify({"error": "Price must be a non-negative number"}), 400

            latitude = data.get("latitude")
            if latitude is None or not isinstance(latitude, (int, float)) or not (-90 <= latitude <= 90):
                return jsonify({"error": "Latitude must be between -90 and 90"}), 400

            longitude = data.get("longitude")
            if longitude is None or not isinstance(longitude, (int, float)) or not (-180 <= longitude <= 180):
                return jsonify({"error": "Longitude must be between -180 and 180"}), 400

            facade = HBnBFacade()
            new_place = facade.create_place(data)
            return jsonify(new_place.to_dict()), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        try:
            facade = HBnBFacade()
            places = facade.get_all_places()
            return [place.to_dict() for place in places], 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        try:
            facade = HBnBFacade()
            result = facade.get_place(place_id)
            if result is None:
                return {"error": "Place not found"}, 404
            return result.to_dict(), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        try:
            data = request.get_json()
            place = Place.query.get(place_id)

            if place is None:
                return {"error": "Place not found"}, 404

            price = data.get("price")
            if price is None or price < 0:
                return jsonify({"error": "Price must be non-negative"}), 400

            latitude = data.get("latitude")
            if latitude is None or not isinstance(latitude, (int, float)) or not (-90 <= latitude <= 90):
                return jsonify({"error": "Latitude must be between -90 and 90"}), 400

            # Update only provided fields
            if "title" in data:
                place.title = data["title"]
            if "price" in data:
                place.price = data["price"]
            if "latitude" in data:
                place.latitude = data["latitude"]
            if "longitude" in data:
                place.longitude = data["longitude"]
            if "description" in data:
                place.description = data["description"]

            place.save()
            return {"message": "Place updated successfully"}, 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500
