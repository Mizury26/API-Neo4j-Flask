from py2neo import Relationship
from app.models.post import Post
from app.models.user import User
from app.models.comment import Comment

class PostController:
    def __init__(self, graph):
        self.graph = graph
    
    def get_all_posts(self):
        """Get all posts"""
        try:
            posts = Post.get_all(self.graph)
            return {"posts": [post.to_dict() for post in posts]}, 200
        except Exception as e:
            return {"error": str(e)}, 500
    
    def get_post_by_id(self, post_id):
        """Get a post by ID"""
        try:
            post = Post.find_by_id(post_id, self.graph)
            if not post:
                return {"error": "Post not found"}, 404
            
            return {"post": post.to_dict()}, 200
        except Exception as e:
            return {"error": str(e)}, 500
    
    def create_post(self, data):
        """Create a new post and link it to a user"""
        try:
            if not data or 'title' not in data or 'content' not in data or 'user_id' not in data:
                return {"error": "Title, content, and user_id are required"}, 400
            
            user = User.find_by_id(data['user_id'], self.graph)
            if not user:
                return {"error": "User not found"}, 404
            
            post = Post(data['title'], data['content'])
            self.graph.create(post)
            
            # Create relationship between User and Post
            relationship = Relationship(user.__node__, "CREATED", post.__node__)
            self.graph.create(relationship)
            
            return {"post": post.to_dict(), "message": "Post created successfully"}, 201
        except Exception as e:
            return {"error": str(e)}, 500
    
    def update_post(self, post_id, data):
        """Update a post by ID"""
        try:
            post = Post.find_by_id(post_id, self.graph)
            if not post:
                return {"error": "Post not found"}, 404
            
            if not data:
                return {"error": "No data provided"}, 400
            
            if 'title' in data:
                post.title = data['title']
            if 'content' in data:
                post.content = data['content']
            
            self.graph.push(post)
            
            return {"post": post.to_dict()}, 200
        except Exception as e:
            return {"error": str(e)}, 500
    
    def delete_post(self, post_id):
        """Delete a post by ID"""
        try:
            post = Post.find_by_id(post_id, self.graph)
            if not post:
                return {"error": "Post not found"}, 404
            
            # Remove all relationships and the node
            self.graph.run(f"MATCH (p:Post {{id: '{post_id}'}}) DETACH DELETE p")
            
            return {"message": "Post deleted successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500
    
    def like_post(self, post_id, data):
        """Like a post"""
        try:
            post = Post.find_by_id(post_id, self.graph)
            if not post:
                return {"error": "Post not found"}, 404
            
            if not data or 'user_id' not in data:
                return {"error": "User ID is required"}, 400
            
            user = User.find_by_id(data['user_id'], self.graph)
            if not user:
                return {"error": "User not found"}, 404
            
            # Check if already liked
            result = self.graph.run(
                f"MATCH (u:User {{id: '{data['user_id']}'}})-[r:LIKES]->(p:Post {{id: '{post_id}'}}) RETURN r"
            ).data()
            
            if result:
                return {"message": "Post already liked by this user"}, 200
            
            relationship = Relationship(user.__node__, "LIKES", post.__node__)
            self.graph.create(relationship)
            
            return {"message": "Post liked successfully"}, 201
        except Exception as e:
            return {"error": str(e)}, 500
    
    def unlike_post(self, post_id, data):
        """Unlike a post"""
        try:
            post = Post.find_by_id(post_id, self.graph)
            if not post:
                return {"error": "Post not found"}, 404
            
            if not data or 'user_id' not in data:
                return {"error": "User ID is required"}, 400
            
            user = User.find_by_id(data['user_id'], self.graph)
            if not user:
                return {"error": "User not found"}, 404
            
            self.graph.run(
                f"MATCH (u:User {{id: '{data['user_id']}'}})-[r:LIKES]->(p:Post {{id: '{post_id}'}}) DELETE r"
            )
            
            return {"message": "Post unliked successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500
    
    def get_post_comments(self, post_id):
        """Get all comments for a post"""
        try:
            post = Post.find_by_id(post_id, self.graph)
            if not post:
                return {"error": "Post not found"}, 404
            
            comments = post.get_comments(self.graph)
            
            return {"comments": [comment.to_dict() for comment in comments]}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    def create_comment(self, post_id, data):
        """Create a comment for a post"""
        try:
            post = Post.find_by_id(post_id, self.graph)
            if not post:
                return {"error": "Post not found"}, 404
            
            if not data or 'content' not in data or 'user_id' not in data:
                return {"error": "Content and user ID are required"}, 400
            
            user = User.find_by_id(data['user_id'], self.graph)
            if not user:
                return {"error": "User not found"}, 404
            
            comment = Comment(data['content'])
            self.graph.create(comment)
            
            # Create relationship between Post and Comment
            relationship = Relationship(post.__node__, "HAS_COMMENT", comment.__node__)
            self.graph.create(relationship)
            
            return {"comment": comment.to_dict(), "message": "Comment created successfully"}, 201
        except Exception as e:
            return {"error": str(e)}, 500

    def get_post_creator(self, post_id):
        """Get the creator of a post"""
        try:
            post = Post.find_by_id(post_id, self.graph)
            if not post:
                return {"error": "Post not found"}, 404
            
            creator = post.get_creator(self.graph)
            if not creator:
                return {"error": "Creator not found"}, 404
            
            return {"creator": creator.to_dict()}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    def get_likes_count(self, post_id):
        """Get the number of likes for a post"""
        try:
            post = Post.find_by_id(post_id, self.graph)
            if not post:
                return {"error": "Post not found"}, 404
            
            count = post.get_likes_count(self.graph)
            
            return {"likes_count": count}, 200
        except Exception as e:
            return {"error": str(e)}, 500
    
    def delete_post_comment(self, post_id, comment_id): 
        """Delete a comment from a post"""
        try:
            post = Post.find_by_id(post_id, self.graph)
            if not post:
                return {"error": "Post not found"}, 404
            
            comment = Comment.find_by_id(comment_id, self.graph)
            if not comment:
                return {"error": "Comment not found"}, 404
            
            self.graph.run(
                f"MATCH (p:Post {{id: '{post_id}'}})-[r:HAS_COMMENT]->(c:Comment {{id: '{comment_id}'}}) DELETE r"
            )
            
            return {"message": "Comment deleted successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500
    
