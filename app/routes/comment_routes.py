from flask import Blueprint, request, jsonify
from app.models.comment import Comment
from app.database import graph
from app.models.user import User
from app.models.post import Post

comment_bp = Blueprint('comment_bp', __name__)

@comment_bp.route('', methods=['GET'])
def get_comments():
    """Get all comments"""
    try:
        comments = Comment.get_all(graph)
        return jsonify([comment.to_dict() for comment in comments]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@comment_bp.route('/<comment_id>', methods=['GET'])
def get_comment(comment_id):
    """Get a comment by ID"""
    try:
        comment = Comment.find_by_id(comment_id, graph)
        if not comment:
            return jsonify({"error": "Comment not found"}), 404
        
        return jsonify(comment.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@comment_bp.route('/<comment_id>', methods=['PUT'])
def update_comment(comment_id):
    """Update a comment by ID"""
    try:
        comment = Comment.find_by_id(comment_id, graph)
        if not comment:
            return jsonify({"error": "Comment not found"}), 404
        
        data = request.get_json()
        if not data or 'content' not in data:
            return jsonify({"error": "Content is required"}), 400
        
        comment.content = data['content']
        graph.push(comment)
        
        return jsonify(comment.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@comment_bp.route('/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    """Delete a comment by ID"""
    try:
        comment = Comment.find_by_id(comment_id, graph)
        if not comment:
            return jsonify({"error": "Comment not found"}), 404
        
        # Delete the comment and its relationships
        graph.run(f"MATCH (c:Comment {{id: '{comment_id}'}}) DETACH DELETE c")
        
        return jsonify({"message": "Comment deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@comment_bp.route('/<comment_id>/like', methods=['POST'])
def like_comment(comment_id):
    """Like a comment"""
    try:
        comment = Comment.find_by_id(comment_id, graph)
        if not comment:
            return jsonify({"error": "Comment not found"}), 404
        
        data = request.get_json()
        if not data or 'user_id' not in data:
            return jsonify({"error": "User ID is required"}), 400
        
        user = User.find_by_id(data['user_id'], graph)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Check if already liked
        result = graph.run(f"MATCH (u:User {{id: '{data['user_id']}'}})-[r:LIKES]->(c:Comment {{id: '{comment_id}'}}) RETURN r").data()
        if result:
            return jsonify({"message": "Comment already liked by this user"}), 200
        
        user.like_comment(comment, graph)
        
        return jsonify({"message": "Comment liked successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@comment_bp.route('/<comment_id>/like', methods=['DELETE'])
def unlike_comment(comment_id):
    """Unlike a comment"""
    try:
        comment = Comment.find_by_id(comment_id, graph)
        if not comment:
            return jsonify({"error": "Comment not found"}), 404
        
        data = request.get_json()
        if not data or 'user_id' not in data:
            return jsonify({"error": "User ID is required"}), 400
        
        user = User.find_by_id(data['user_id'], graph)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        user.unlike_comment(comment, graph)
        
        return jsonify({"message": "Comment unliked successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500