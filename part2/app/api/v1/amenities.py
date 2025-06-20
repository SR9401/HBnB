from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import jsonify, request

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        try:
            amenity_data = api.payload
            if not amenity_data or 'name' not in amenity_data:
                return {'error': "Missing 'name' field"}, 400

            existing_amenities = facade.get_all_amenities()
            if any(a['name'] == amenity_data['name'] for a in existing_amenities):
                return {'error': 'Amenity is already registered'}, 400

            new_amenity = facade.create_amenity(amenity_data)

            return {
                'id': new_amenity.id,
                'name': new_amenity.name
            }, 201
        except Exception as e:
            return {'error': f'Internal server error: {str(e)}'}, 500

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        try:
            result = facade.get_all_amenities()
            return jsonify(result), 200
        except Exception as e:
            return {'error': f'Failed to retrieve amenities: {str(e)}'}, 500

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        try:
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                return {'error': 'Amenity not found'}, 404

            return {
                'id': amenity.id,
                'name': amenity.name
            }, 200
        except Exception as e:
            return {'error': f'Failed to retrieve amenity: {str(e)}'}, 500

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        try:
            data = request.get_json()
            if not data or 'name' not in data:
                return {'error': "Missing 'name' field in the input data"}, 400

            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                return {'error': 'Amenity not found'}, 404

            amenity.update(data)

            return {
                'id': amenity.id,
                'name': amenity.name
            }, 200
        except Exception as e:
            return {'error': f'Failed to update amenity: {str(e)}'}, 500
