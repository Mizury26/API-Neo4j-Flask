from flask import Blueprint, request, jsonify
from app.controllers.comment_controller import CommentController
from app.database import graph

comment_bp = Blueprint('comment_bp', __name__)
controller = CommentController(graph)

@comment_bp.route('', methods=['GET'])
def get_comments():
    """Get all comments"""
    result, status_code = controller.get_all_comments()
    return jsonify(result), status_code

@comment_bp.route('/<comment_id>', methods=['GET'])
def get_comment(comment_id):
    """Get a comment by ID"""
    result, status_code = controller.get_comment_by_id(comment_id)
    return jsonify(result), status_code

@comment_bp.route('/<comment_id>', methods=['PUT'])
def update_comment(comment_id):
    """Update a comment by ID"""
    data = request.get_json()
    result, status_code = controller.update_comment(comment_id, data)
    return jsonify(result), status_code

@comment_bp.route('/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    """Delete a comment by ID"""
    result, status_code = controller.delete_comment(comment_id)
    return jsonify(result), status_code

@comment_bp.route('/<comment_id>/like', methods=['POST'])
def like_comment(comment_id):
    """Like a comment"""
    data = request.get_json()
    result, status_code = controller.like_comment(comment_id, data)
    return jsonify(result), status_code

@comment_bp.route('/<comment_id>/like', methods=['DELETE'])
def unlike_comment(comment_id):
    """Unlike a comment"""
    data = request.get_json()
    result, status_code = controller.unlike_comment(comment_id, data)
    return jsonify(result), status_code

@comment_bp.route('', methods=['POST'])
def create_comment():
    """Create a new comment"""
    data = request.get_json()
    result, status_code = controller.create_comment(data)
    return jsonify(result), status_code