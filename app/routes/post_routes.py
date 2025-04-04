from flask import Blueprint, request, jsonify
from app.controllers.post_controller import PostController
from app.database import graph

post_bp = Blueprint('post_bp', __name__)
controller = PostController(graph)

@post_bp.route('', methods=['GET'])
def get_posts():
    """Get all posts"""
    result, status_code = controller.get_all_posts()
    return jsonify(result), status_code

@post_bp.route('/<post_id>', methods=['GET'])
def get_post(post_id):
    """Get a post by ID"""
    result, status_code = controller.get_post_by_id(post_id)
    return jsonify(result), status_code

@post_bp.route('', methods=['POST'])
def create_post():
    """Create a new post"""
    data = request.get_json()
    result, status_code = controller.create_post(data)
    return jsonify(result), status_code

@post_bp.route('/<post_id>', methods=['PUT'])
def update_post(post_id):
    """Update a post by ID"""
    data = request.get_json()
    result, status_code = controller.update_post(post_id, data)
    return jsonify(result), status_code

@post_bp.route('/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a post by ID"""
    result, status_code = controller.delete_post(post_id)
    return jsonify(result), status_code

@post_bp.route('/<post_id>/like', methods=['POST'])
def like_post(post_id):
    """Like a post"""
    data = request.get_json()
    result, status_code = controller.like_post(post_id, data)
    return jsonify(result), status_code

@post_bp.route('/<post_id>/like', methods=['DELETE'])
def unlike_post(post_id):
    """Unlike a post"""
    data = request.get_json()
    result, status_code = controller.unlike_post(post_id, data)
    return jsonify(result), status_code

@post_bp.route('/<post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    """Get all comments for a post"""
    result, status_code = controller.get_post_comments(post_id)
    return jsonify(result), status_code

@post_bp.route('/<post_id>/comments', methods=['POST'])
def create_comment(post_id):
    """Create a comment for a post"""
    data = request.get_json()
    result, status_code = controller.create_comment(post_id, data)
    return jsonify(result), status_code

@post_bp.route('/<post_id>/comments/<comment_id>', methods=['DELETE'])
def delete_post_comment(post_id, comment_id):
    """Delete a comment from a post"""
    result, status_code = controller.delete_post_comment(post_id, comment_id)
    return jsonify(result), status_code