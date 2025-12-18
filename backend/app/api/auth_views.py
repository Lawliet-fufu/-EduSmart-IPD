from flask import request, jsonify
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import SQLAlchemyError
from . import auth
from app import db
from app.models import User, UserPreferences
from app.utils.decorators import jwt_required, get_current_user
import traceback


@auth.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json() or {}
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Username and password are required'}), 400

        # Try to query user from database
        try:
            user = User.query.filter_by(username=username).first()
        except SQLAlchemyError as e:
            # Database connection error
            print(f"Database error during login: {str(e)}")
            print(traceback.format_exc())
            return jsonify({
                'message': 'Database connection error. Please check database configuration and ensure MySQL is running.',
                'error': str(e)
            }), 500

        if not user or not _verify_password(user.password_hash, password):
            return jsonify({'message': 'Invalid username or password'}), 401

        additional_claims = {'role': user.role}
        # JWT identity (sub field) must be a string
        access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)

        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'full_name': user.full_name,
                'role': user.role,
                'email': user.email,
                'avatar': user.avatar,
            }
        }), 200
    except Exception as e:
        # Catch any other unexpected errors
        print(f"Unexpected error during login: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'message': 'An unexpected error occurred',
            'error': str(e)
        }), 500


@auth.route('/me', methods=['GET'])
@jwt_required
def me():
    user = get_current_user()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({
        'id': user.id,
        'username': user.username,
        'full_name': user.full_name,
        'role': user.role,
        'email': user.email,
        'avatar': user.avatar,
    }), 200


@auth.route('/preferences', methods=['GET'])
@jwt_required
def get_preferences():
    pass


@auth.route('/preferences', methods=['PUT'])
@jwt_required
def update_preferences():
    pass


def _verify_password(stored_hash: str, raw_password: str) -> bool:
    """
    Simple password verification helper.

    - If stored_hash starts with 'hashed:', treat the suffix as plain text for demo purposes.
    - Otherwise, compare directly (you can later replace with real hashing like werkzeug.security).
    """
    if not stored_hash:
        return False

    if stored_hash.startswith('hashed:'):
        return stored_hash[len('hashed:'):] == raw_password

    # Fallback: direct comparison
    return stored_hash == raw_password
