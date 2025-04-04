from py2neo import Node, Relationship
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom
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

    def create_with_user(self, user, graph):
        graph.create(self.__node__)
        relationship = Relationship(user.__node__, "CREATED", self.__node__)
        graph.create(relationship)
        return self

    def get_creator(self, graph):
        result = graph.run(
            f"MATCH (u:User)-[:CREATED]->(p:Post {{id: '{self.id}'}}) RETURN u"
        ).data()
        if result:
            return User.wrap(result[0]["u"])
        return None

    def get_comments(self, graph):
        from app.models.comment import Comment
        result = graph.run(
            f"MATCH (p:Post {{id: '{self.id}'}})-[:HAS_COMMENT]->(c:Comment) RETURN c"
        ).data()
        return [Comment.wrap(record["c"]) for record in result]

    def get_likes_count(self, graph):
        result = graph.run(
            f"MATCH (u:User)-[:LIKES]->(p:Post {{id: '{self.id}'}}) RETURN count(u) as count"
        ).data()
        if result:
            return result[0]["count"]
        return 0

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
