from flask import Blueprint, request, jsonify, make_response
from flask_security import SQLAlchemyUserDatastore, utils, auth_required
from flask_restful import Api, Resource
from backend.models import db, Users, Roles, Admin
from datetime import datetime
from flask_login import current_user
from flask_security.utils import login_user

auth_bp = Blueprint('auth', __name__)
api = Api(auth_bp)
user_datastore = SQLAlchemyUserDatastore(db, Users, Roles)

class Register(Resource):
    def post(self):
        data = request.get_json()
        if 'email' not in data or 'password' not in data:
            return make_response(jsonify({'message': 'Email and Password are required fields'}), 400)
        if 'username' not in data:
            return make_response(jsonify({'message': 'Username cannot be empty'}), 400)
        email = data['email']
        username = data['username']
        password = utils.hash_password(data['password'])
        if user_datastore.find_user(email=email):
            return make_response(jsonify({'message': 'User already exists'}), 400)
        user_role = user_datastore.find_role('user')
        user = user_datastore.create_user(
            email=email,
            password=password,
            username=username,
            confirmed_at=datetime.utcnow(),
            roles=[user_role]
        )
        db.session.commit()
        return make_response(jsonify({'message': 'User created', 'email': user.email}), 201)

class Login(Resource):
    def post(self):
        data = request.get_json(force=True)
        email = data.get('email')
        password = data.get('password')
        user = user_datastore.find_user(email=email)
        if not user or not utils.verify_password(password, user.password):
            return make_response(jsonify({'message': 'Invalid credentials'}), 401)
        
        # Establish session for Flask-Security
        login_user(user, remember=True)  # remember=True optional
        
        return make_response(jsonify({
            'success': True,
            'message': 'User login successful',
            'email': user.email,
            'username': user.username
        }), 200)

class AdminLogin(Resource):
    def post(self):
        data = request.get_json(force=True)
        email = data.get('email')
        password = data.get('password')
        admin = Admin.query.filter_by(email=email).first()
        if not admin or not utils.verify_password(password, admin.password):
            return make_response(jsonify({'message': 'Invalid admin credentials'}), 401)
        return make_response(jsonify({
            'success': True,
            'message': 'Admin login successful',
            'email': admin.email,
            'username': admin.username
        }), 200)

class Logout(Resource):
    @auth_required()
    def post(self):
        utils.logout_user()
        return make_response(jsonify({'success': True, 'message': 'Logout successful'}), 200)

class UserProfile(Resource):
    @auth_required()
    def get(self):
        user_data = {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
        }
        return make_response(jsonify(user_data), 200)

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(AdminLogin, '/admin-login')
api.add_resource(Logout, '/logout')
api.add_resource(UserProfile, '/user')
