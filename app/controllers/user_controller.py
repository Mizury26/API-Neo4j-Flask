from py2neo import Relationship, Node
from app.models.user import User
from app.models.post import Post

class UserController:
    def __init__(self, graph):
        self.graph = graph

    def get_all_users(self):
        """Get all users"""
        try:
            users = User.get_all(self.graph)
            return {"users": [user.to_dict() for user in users]}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    def get_user_by_id(self, user_id):
        """Get a user by ID"""
        try:
            user = User.find_by_id(user_id, self.graph)
            if not user:
                return {"error": "User not found"}, 404
            return {"user": user.to_dict()}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    def create_user(self, data):
        """Create a new user"""
        try:
            if not data or 'name' not in data or 'email' not in data:
                return {"error": "Name and email are required"}, 400
            
            existing_user = self.graph.run(f"MATCH (u:User {{email: '{data['email']}'}}) RETURN u").data()
            if existing_user:
                return {"error": "Email already registered"}, 400
            
            user = User(data['name'], data['email'])
            self.graph.create(user)
            
            return {"user": user.to_dict(), "message": "User created successfully"}, 201
        except Exception as e:
            return {"error": str(e)}, 500

    def update_user(self, user_id, data):
        """Update a user's details"""
        try:
            user = User.find_by_id(user_id, self.graph)
            if not user:
                return {"error": "User not found"}, 404
            
            if not data:
                return {"error": "No data provided"}, 400
            
            if 'name' in data:
                user.name = data['name']
            if 'email' in data:
                user.email = data['email']
            
            self.graph.push(user)
            
            return {"user": user.to_dict()}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    def delete_user(self, user_id):
        """Delete a user"""
        try:
            user = User.find_by_id(user_id, self.graph)
            if not user:
                return {"error": "User not found"}, 404
            
            # Remove all relationships before deleting the node
            self.graph.run(f"MATCH (u:User {{id: '{user_id}'}}) DETACH DELETE u")
            
            return {"message": "User deleted successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    def get_user_posts(self, user_id):
        """Get all posts created by a user"""
        try:
            user = User.find_by_id(user_id, self.graph)
            if not user:
                return {"error": "User not found"}, 404
            
            posts = Post.get_by_user(user_id, self.graph)
            
            return {"posts": [post.to_dict() for post in posts]}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    def get_user_friends(self, user_id):
        """Get all friends of a user"""
        try:
            user = User.find_by_id(user_id, self.graph)
            if not user:
                return {"error": "User not found"}, 404
            
            result = self.graph.run(f"MATCH (u:User {{id: '{user_id}'}})-[:FRIENDS_WITH]->(f:User) RETURN f").data()
            friends = [User.wrap(record["f"]) for record in result]
            
            return {"friends": [friend.to_dict() for friend in friends]}, 200
        except Exception as e:
            return {"error": str(e)}, 500
    
    def check_friendship(self, user_id, friend_id):
        """Check if two users are friends"""
        try:
            user = User.find_by_id(user_id, self.graph)
            friend = User.find_by_id(friend_id, self.graph)
            
            if not user or not friend:
                return {"error": "User or friend not found"}, 404
            
            result = self.graph.run(
                f"MATCH (u:User {{id: '{user_id}'}})-[r:FRIENDS_WITH]->(f:User {{id: '{friend_id}'}}) RETURN r"
            ).data()
            
            if result:
                return {"message": "They are friends"}, 200
            else:
                return {"message": "They are not friends"}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    def add_friend(self, user_id, data):
        """Add a friend to a user"""
        try:
            if not data or 'friend_id' not in data:
                return {"error": "Friend ID is required"}, 400
            
            user = User.find_by_id(user_id, self.graph)
            friend = User.find_by_id(data['friend_id'], self.graph)
            
            if not user or not friend:
                return {"error": "User or friend not found"}, 404
            
            # Check if they are already friends
            result = self.graph.run(
                f"MATCH (u:User {{id: '{user_id}'}})-[r:FRIENDS_WITH]->(f:User {{id: '{data['friend_id']}'}}) RETURN r"
            ).data()
            
            if result:
                return {"message": "Already friends"}, 200
            
            relationship = Relationship(user.__node__, "FRIENDS_WITH", friend.__node__)
            self.graph.create(relationship)
            
            return {"message": "Friend added successfully"}, 201
        except Exception as e:
            return {"error": str(e)}, 500

    def remove_friend(self, user_id, data):
        """Remove a friend"""
        try:
            if not data or 'friend_id' not in data:
                return {"error": "Friend ID is required"}, 400
            
            user = User.find_by_id(user_id, self.graph)
            friend = User.find_by_id(data['friend_id'], self.graph)
            
            if not user or not friend:
                return {"error": "User or friend not found"}, 404
            
            self.graph.run(
                f"MATCH (u:User {{id: '{user_id}'}})-[r:FRIENDS_WITH]->(f:User {{id: '{data['friend_id']}'}}) DELETE r"
            )
            
            return {"message": "Friend removed successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        
    def get_mutual_friends(self, user_id, other_id):
        """Get mutual friends between two users"""
        try:
            user = User.find_by_id(user_id, self.graph)
            other_user = User.find_by_id(other_id, self.graph)
            
            if not user or not other_user:
                return {"error": "User or other user not found"}, 404
            
            result = self.graph.run(
                f"MATCH (u:User {{id: '{user_id}'}})-[:FRIENDS_WITH]->(f:User)<-[:FRIENDS_WITH]-(o:User {{id: '{other_id}'}}) RETURN f"
            ).data()
            
            mutual_friends = [User.wrap(record["f"]) for record in result]
            
            return {"mutual_friends": [friend.to_dict() for friend in mutual_friends]}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    def get_user_likes(self, user_id):
        """Get all posts liked by a user"""
        try:
            user = User.find_by_id(user_id, self.graph)
            if not user:
                return {"error": "User not found"}, 404
            
            result = self.graph.run(
                f"MATCH (u:User {{id: '{user_id}'}})-[:LIKES]->(p:Post) RETURN p"
            ).data()
            
            liked_posts = [Post.wrap(record["p"]) for record in result]
            
            return {"liked_posts": [post.to_dict() for post in liked_posts]}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        
    def add_user_post(self, user_id, data):
        """Add a post for a user"""
        try:
            if not data or 'content' not in data:
                return {"error": "Content is required"}, 400
            
            user = User.find_by_id(user_id, self.graph)
            if not user:
                return {"error": "User not found"}, 404
            
            post = Post(data['content'])
            post_node = Node("Post", id=post.id, content=post.content, created_at=post.created_at)
            self.graph.create(post_node)
            
            self.graph.create(Relationship(user.__node__, "CREATED", post_node))
            
            return {"post": post.to_dict(), "message": "Post created successfully"}, 201
        except Exception as e:
            return {"error": str(e)}, 500
