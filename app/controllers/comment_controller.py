from app.models.comment import Comment
from py2neo import Graph, Node, Relationship


class CommentController:
    def __init__(self, graph: Graph):
        self.graph = graph

    def get_all_comments(self):
        try:
            comments = Comment.get_all(self.graph)
            return {"comments": [comment.to_dict() for comment in comments]}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    def get_comment_by_id(self, comment_id):
        try:
            comment = Comment.find_by_id(self.graph, comment_id)
            if not comment:
                return {"error": "Comment not found"}, 404
            return {"comment": comment.to_dict()}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    def create_comment(self, data):
        try:
            if not all(key in data for key in ['content', 'user_id', 'post_id']):
                return {"error": "Content, user_id, and post_id are required"}, 400

            user = self.graph.evaluate("MATCH (u:User {id: $user_id}) RETURN u", user_id=data['user_id'])
            post = self.graph.evaluate("MATCH (p:Post {id: $post_id}) RETURN p", post_id=data['post_id'])
            
            if not user:
                return {"error": "User not found"}, 404
            if not post:
                return {"error": "Post not found"}, 404

            comment = Comment(data['content'])
            comment_node = Node("Comment", id=comment.id, content=comment.content, created_at=comment.created_at)
            self.graph.create(comment_node)
            
            self.graph.create(Relationship(user, "CREATED", comment_node))
            self.graph.create(Relationship(post, "HAS_COMMENT", comment_node))

            return {"comment": comment.to_dict(), "message": "Comment created successfully"}, 201
        except Exception as e:
            return {"error": str(e)}, 500

    def delete_comment(self, comment_id):
        try:
            comment = Comment.find_by_id(self.graph, comment_id)
            if not comment:
                return {"error": "Comment not found"}, 404
            self.graph.run("MATCH (c:Comment {id: $id}) DETACH DELETE c", id=comment_id)
            return {"message": "Comment deleted successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500
    
    def update_comment(self, comment_id, data):
        try:
            comment = Comment.find_by_id(self.graph, comment_id)
            if not comment:
                return {"error": "Comment not found"}, 404
            
            if 'content' in data:
                comment.content = data['content']
                self.graph.push(comment)
            
            return {"comment": comment.to_dict(), "message": "Comment updated successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    def like_comment(self, comment_id, user_id):
        try:
            user = self.graph.evaluate("MATCH (u:User {id: $user_id}) RETURN u", user_id=user_id)
            comment = self.graph.evaluate("MATCH (c:Comment {id: $comment_id}) RETURN c", comment_id=comment_id)
            if not user or not comment:
                return {"error": "User or Comment not found"}, 404
            
            existing_like = self.graph.evaluate(
                "MATCH (u:User {id: $user_id})-[r:LIKES]->(c:Comment {id: $comment_id}) RETURN r",
                user_id=user_id, comment_id=comment_id
            )
            if existing_like:
                return {"message": "Comment already liked by this user"}, 200

            self.graph.create(Relationship(user, "LIKES", comment))
            return {"message": "Comment liked successfully"}, 201
        except Exception as e:
            return {"error": str(e)}, 500

    def unlike_comment(self, comment_id, user_id):
        try:
            self.graph.run(
                "MATCH (u:User {id: $user_id})-[r:LIKES]->(c:Comment {id: $comment_id}) DELETE r",
                user_id=user_id, comment_id=comment_id
            )
            return {"message": "Comment unliked successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500
