from flask import Blueprint, request, jsonify
from app.models.user import User
from app.models.post import Post
from app.database import graph
from app.controllers.user_controller import UserController

user_bp = Blueprint('user_bp', __name__)
controller = UserController(graph)

@user_bp.route('', methods=['GET'])
def get_users():
    """Get all users"""
    try:
        result, status_code = controller.get_all_posts()
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get a user by ID"""
    try:
        result, status_code = controller.get_user_by_id(user_id)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('', methods=['POST'])
def create_user(data):
    """Create a new user"""
    try:
        data = request.get_json()
        result, status_code = controller.create_post(data)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@user_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a user by ID"""
    try :
        result, status_code = controller.update_post(user_id)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user by ID"""
    try:
        result, status_code = controller.delete_post(user_id)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/<user_id>/friends', methods=['GET'])
def get_friends(user_id):
    """Get all friends of a user"""
    try:
        result, status_code = controller.get_user_friends(user_id)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/<user_id>/friends', methods=['POST'])
def add_friend(user_id):
    """Add a friend to a user"""
    try:
        result, status_code = controller.add_friend(user_id)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/<user_id>/friends/<friend_id>', methods=['DELETE'])
def remove_friend(user_id, friend_id):
    """Remove a friend from a user"""
    try:
        result, status_code = controller.remove_friend(user_id, friend_id)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/<user_id>/friends/<friend_id>', methods=['GET'])
def check_friendship(user_id, friend_id):
    """Check if two users are friends"""
    try:
        result, status_code = controller.check_friendship(user_id, friend_id)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/<user_id>/mutual-friends/<other_id>', methods=['GET'])
def get_mutual_friends(user_id, other_id):
    """Get mutual friends between two users"""
    try:
        result, status_code = controller.get_mutual_friends(user_id, other_id)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/<user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    """Get all posts by a user"""
    try:
        result, status_code = controller.get_user_posts(user_id)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/<user_id>/posts', methods=['POST'])
def create_post(user_id, data):
    """Create a post for a user"""
    try:
        result, status_code = controller.add_user_post(user_id, data)
        return jsonify(result), status_code        
    except Exception as e:
        return jsonify({"error": str(e)}), 500