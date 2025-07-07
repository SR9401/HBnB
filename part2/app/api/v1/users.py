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
        """Update user - Admins can modify anyone, users can modify themselves (limited)"""
        claims = get_jwt()
        current_user_id = get_jwt_identity()
        user_data = api.payload
        is_admin = claims.get('is_admin', False)
        # Récupère l'utilisateur cible
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        if is_admin:
            # Admin : accès complet
            try:
                facade.update_user(user_id, user_data)
                updated_user = facade.get_user(user_id)
                return updated_user.to_dict(), 200
            except Exception as e:
                return {'error': str(e)}, 400
        else:
            # Utilisateur : peut seulement modifier ses propres données (sauf email et password)
            if user_id != current_user_id:
                return {'error': 'Unauthorized action'}, 403
            forbidden_fields = ['email', 'password', 'is_admin']
        for field in forbidden_fields:
            if field in user_data and user_data[field] != getattr(user, field):
                return {'error': f"You cannot modify the field '{field}'."}, 400
            try:
                facade.update_user(user_id, user_data)
                return {'message': 'User updated successfully'}, 200
            except Exception as e:
                return {'error': str(e)}, 400