from flask_restx import Namespace, Resource, fields, abort
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Entrez 'Bearer ' suivi de votre token JWT"
    }
}

api = Namespace('users', description='User operations', authorizations=authorizations, security='Bearer Auth')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'is_admin': fields.Boolean(required=False, description='Set to true to create an admin user', default=False)
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(409, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 409
        
        all_users = facade.get_users()
        if not all_users:
            user_data['is_admin'] = True
        else:
            claims = get_jwt() if get_jwt_identity() else {}
            if not claims or not claims.get('is_admin'):
                api.abort(403, 'Admin privileges required.')
            user_data['is_admin'] = False

        try:
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400
        
    @jwt_required()
    @api.doc(security='Bearer Auth')
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of users (admin only)"""
        claims = get_jwt()
        if not claims.get('is_admin'):
            abort(403, 'Admin privileges required')

        users = facade.get_users()
        return [user.to_dict() for user in users], 200
    
@api.route('/<user_id>')
class UserResource(Resource):
    @jwt_required()
    @api.doc(security='Bearer Auth')
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user by ID (admin only)"""
        claims = get_jwt()
        if not claims.get('is_admin'):
            abort(403, 'Admin privileges required')

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @jwt_required()
    @api.doc(security='Bearer Auth')
    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user (admin only)"""
        claims = get_jwt()
        if not claims.get('is_admin'):
            abort(403, 'Admin privileges required')

        user_data = api.payload
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        try:
            facade.update_user(user_id, user_data)
            update_user = facade.get_user(user_id)
            return update_user.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400
