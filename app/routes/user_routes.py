from flask import Blueprint, request, jsonify
from app.models.user import User
from app.models.post import Post
from app.database import graph

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('', methods=['GET'])
def get_users():
    """Get all users"""
    try:
        users = User.get_all(graph)
        return jsonify([user.to_dict() for user in users]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        if not data or 'name' not in data or 'email' not in data:
            return jsonify({"error": "Name and email are required"}), 400
        
        user = User(data['name'], data['email'])
        graph.create(user)
        
        return jsonify(user.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get a user by ID"""
    try:
        user = User.find_by_id(user_id, graph)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a user by ID"""
    try:
        user = User.find_by_id(user_id, graph)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            user.email = data['email']
        
        graph.push(user)
        
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user by ID"""
    try:
        user = User.find_by_id(user_id, graph)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Remove all relationships and the node
        graph.run(f"MATCH (u:User {{id: '{user_id}'}}) DETACH DELETE u")
        
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/<user_id>/friends', methods=['GET'])
def get_friends(user_id):
    """Get all friends of a user"""
    try:
        user = User.find_by_id(user_id, graph)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        friends = user.get_friends(graph)
        return jsonify([friend.to_dict() for friend in friends]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/<user_id>/friends', methods=['POST'])
def add_friend(user_id):
    """Add a friend to a user"""
    try:
        user = User.find_by_id(user_id, graph)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        data = request.get_json()
        if not data or 'friend_id' not in data:
            return jsonify({"error": "Friend ID is required"}), 400
        
        friend = User.find_by_id(data['friend_id'], graph)
        if not friend:
            return jsonify({"error": "Friend not found"}), 404
        
        # Check if already friends
        if user.is_friend_with(friend, graph):
            return jsonify({"message": "Users are already friends"}), 200
        
        user.add_friend(friend, graph)
        
        return jsonify({"message": "Friend added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/<user_id>/friends/<friend_id>', methods=['DELETE'])
def remove_friend(user_id, friend_id):
    """Remove a friend from a user"""
    try:
        user = User.find_by_id(user_id, graph)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        friend = User.find_by_id(friend_id, graph)
        if not friend:
            return jsonify({"error": "Friend not found"}), 404
        
        user.remove_friend(friend, graph)
        
        return jsonify({"message": "Friend removed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/<user_id>/friends/<friend_id>', methods=['GET'])
def check_friendship(user_id, friend_id):
    """Check if two users are friends"""
    try:
        user = User.find_by_id(user_id, graph)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        friend = User.find_by_id(friend_id, graph)
        if not friend:
            return jsonify({"error": "Friend not found"}), 404
        
        is_friend = user.is_friend_with(friend, graph)
        
        return jsonify({"are_friends": is_friend}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/<user_id>/mutual-friends/<other_id>', methods=['GET'])
def get_mutual_friends(user_id, other_id):
    """Get mutual friends between two users"""
    try:
        user = User.find_by_id(user_id, graph)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        other_user = User.find_by_id(other_id, graph)
        if not other_user:
            return jsonify({"error": "Other user not found"}), 404
        
        mutual_friends = user.get_mutual_friends(other_user, graph)
        
        return jsonify([friend.to_dict() for friend in mutual_friends]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/<user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    """Get all posts by a user"""
    try:
        user = User.find_by_id(user_id, graph)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        posts = Post.get_by_user(user_id, graph)
        
        return jsonify([post.to_dict() for post in posts]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/<user_id>/posts', methods=['POST'])
def create_post(user_id):
    """Create a post for a user"""
    try:
        user = User.find_by_id(user_id, graph)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        data = request.get_json()
        if not data or 'title' not in data or 'content' not in data:
            return jsonify({"error": "Title and content are required"}), 400
        
        post = Post(data['title'], data['content'])
        post.create_with_user(user, graph)
        
        return jsonify(post.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500