from py2neo import Node, Relationship
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom
from datetime import datetime
import uuid
from app.models.user import User

class Comment(GraphObject):
    __primarylabel__ = "Comment"
    __primarykey__ = "id"

    id = Property()
    content = Property()
    created_at = Property()

    # Relationships
    created_by = RelatedFrom("User", "CREATED")
    post = RelatedFrom("Post", "HAS_COMMENT")
    liked_by = RelatedFrom("User", "LIKES")

    def __init__(self, content):
        self.id = str(uuid.uuid4())
        self.content = content
        self.created_at = datetime.now().timestamp()

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "created_at": self.created_at
        }
    
    def create_with_user_and_post(self, user, post, graph):
        graph.create(self.__node__)
        
        # Create relationship with user (CREATED)
        user_rel = Relationship(user.__node__, "CREATED", self.__node__)
        graph.create(user_rel)
        
        # Create relationship with post (HAS_COMMENT)
        post_rel = Relationship(post.__node__, "HAS_COMMENT", self.__node__)
        graph.create(post_rel)
        
        return self
    
    def get_creator(self, graph):
        result = graph.run(f"MATCH (u:User)-[:CREATED]->(c:Comment {{id: '{self.id}'}}) RETURN u").data()
        if result:
            return User.wrap(result[0]['u'])
        return None
    
    def get_post(self, graph):
        from app.models.post import Post

        result = graph.run(f"MATCH (p:Post)-[:HAS_COMMENT]->(c:Comment {{id: '{self.id}'}}) RETURN p").data()
        if result:
            return Post.wrap(result[0]['p'])
        return None
    
    def get_likes_count(self, graph):
        result = graph.run(f"MATCH (u:User)-[:LIKES]->(c:Comment {{id: '{self.id}'}}) RETURN count(u) as count").data()
        if result:
            return result[0]['count']
        return 0
    
    @staticmethod
    def find_by_id(comment_id, graph):
        result = graph.run(f"MATCH (c:Comment {{id: '{comment_id}'}}) RETURN c").data()
        if result:
            return Comment.wrap(result[0]['c'])
        return None
    
    @staticmethod
    def get_all(graph):
        result = graph.run("MATCH (c:Comment) RETURN c").data()
        return [Comment.wrap(record['c']) for record in result]
    
    @staticmethod
    def get_by_post(post_id, graph):
        result = graph.run(f"MATCH (p:Post {{id: '{post_id}'}})-[:HAS_COMMENT]->(c:Comment) RETURN c").data()
        return [Comment.wrap(record['c']) for record in result]