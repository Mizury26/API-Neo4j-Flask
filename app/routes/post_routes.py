from flask import Blueprint, request, jsonify
from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User
from app.database import graph

post_bp = Blueprint('post_bp', __name__)

@post_bp.route('', methods=['GET'])
def get_posts():
    """Get all posts"""
    try:
        posts = Post.get_all(graph)
        return jsonify([post.to_dict() for post in posts]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@post_bp.route('/<post_id>', methods=['GET'])
def get_post(post_id):
    """Get a post by ID"""
    try:
        post = Post.find_by_id(post_id, graph)
        if not post:
            return jsonify({"error": "Post not found"}), 404
        
        return jsonify(post.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@post_bp.route('/<post_id>', methods=['PUT'])
def update_post(post_id):
    """Update a post by ID"""
    try:
        post = Post.find_by_id(post_id, graph)
        if not post:
            return jsonify({"error": "Post not found"}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        if 'title' in data:
            post.title = data['title']
        if 'content' in data:
            post.content = data['content']
        
        graph.push(post)
        
        return jsonify(post.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@post_bp.route('/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a post by ID"""
    try:
        post = Post.find_by_id(post_id, graph)
        if not post:
            return jsonify({"error": "Post not found"}), 404
        
        # Remove all relationships and the node
        graph.run(f"MATCH (p:Post {{id: '{post_id}'}}) DETACH DELETE p")
        
        return jsonify({"message": "Post deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@post_bp.route('/<post_id>/like', methods=['POST'])
def like_post(post_id):
    """Like a post"""
    try:
        post = Post.find_by_id(post_id, graph)
        if not post:
            return jsonify({"error": "Post not found"}), 404
        
        data = request.get_json()
        if not data or 'user_id' not in data:
            return jsonify({"error": "User ID is required"}), 400
        
        user = User.find_by_id(data['user_id'], graph)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Check if already liked
        result = graph.run(f"MATCH (u:User {{id: '{data['user_id']}'}})-[r:LIKES]->(p:Post {{id: '{post_id}'}}) RETURN r").data()
        if result:
            return jsonify({"message": "Post already liked by this user"}), 200
        
        user.like_post(post, graph)
        
        return jsonify({"message": "Post liked successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@post_bp.route('/<post_id>/like', methods=['DELETE'])
def unlike_post(post_id):
    """Unlike a post"""
    try:
        post = Post.find_by_id(post_id, graph)
        if not post:
            return jsonify({"error": "Post not found"}), 404
        
        data = request.get_json()
        if not data or 'user_id' not in data:
            return jsonify({"error": "User ID is required"}), 400
        
        user = User.find_by_id(data['user_id'], graph)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        user.unlike_post(post, graph)
        
        return jsonify({"message": "Post unliked successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@post_bp.route('/<post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    """Get all comments for a post"""
    try:
        post = Post.find_by_id(post_id, graph)
        if not post:
            return jsonify({"error": "Post not found"}), 404
        
        comments = post.get_comments(graph)
        
        return jsonify([comment.to_dict() for comment in comments]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@post_bp.route('/<post_id>/comments', methods=['POST'])
def create_comment(post_id):
    """Create a comment for a post"""
    try:
        post = Post.find_by_id(post_id, graph)
        if not post:
            return jsonify({"error": "Post not found"}), 404
        
        data = request.get_json()
        if not data or 'content' not in data or 'user_id' not in data:
            return jsonify({"error": "Content and user ID are required"}), 400
        
        user = User.find_by_id(data['user_id'], graph)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        comment = Comment(data['content'])
        comment.create_with_user_and_post(user, post, graph)
        
        return jsonify(comment.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@post_bp.route('/<post_id>/comments/<comment_id>', methods=['DELETE'])
def delete_post_comment(post_id, comment_id):
    """Delete a comment from a post"""
    try:
        post = Post.find_by_id(post_id, graph)
        if not post:
            return jsonify({"error": "Post not found"}), 404
        
        comment = Comment.find_by_id(comment_id, graph)
        if not comment:
            return jsonify({"error": "Comment not found"}), 404
        
        # Check if comment belongs to post
        result = graph.run(f"MATCH (p:Post {{id: '{post_id}'}})-[:HAS_COMMENT]->(c:Comment {{id: '{comment_id}'}}) RETURN c").data()
        if not result:
            return jsonify({"error": "Comment does not belong to this post"}), 400
        
        # Delete the comment and its relationships
        graph.run(f"MATCH (c:Comment {{id: '{comment_id}'}}) DETACH DELETE c")
        
        return jsonify({"message": "Comment deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500