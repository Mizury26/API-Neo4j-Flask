from py2neo.ogm import GraphObject, Property, RelatedFrom
from datetime import datetime
import uuid
from app.models.user import User


class Post(GraphObject):
    __primarylabel__ = "Post"
    __primarykey__ = "id"

    id = Property()
    title = Property()
    content = Property()
    created_at = Property()

    # Relationships
    created_by = RelatedFrom("User", "CREATED")
    comments = RelatedFrom("Comment", "HAS_COMMENT")
    liked_by = RelatedFrom("User", "LIKES")

    def __init__(self, title, content, user=None):
        self.id = str(uuid.uuid4())
        self.title = title
        self.content = content
        self.created_at = datetime.now().timestamp()
        self.user = user

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at,
        }

    @staticmethod
    def find_by_id(post_id, graph):
        result = graph.run(f"MATCH (p:Post {{id: '{post_id}'}}) RETURN p").data()
        if result:
            return Post.wrap(result[0]["p"])
        return None

    @staticmethod
    def get_all(graph):
        result = graph.run("MATCH (p:Post) RETURN p").data()
        return [Post.wrap(record["p"]) for record in result]

    @staticmethod
    def get_by_user(user_id, graph):
        result = graph.run(
            f"MATCH (u:User {{id: '{user_id}'}})-[:CREATED]->(p:Post) RETURN p"
        ).data()
        return [Post.wrap(record["p"]) for record in result]
