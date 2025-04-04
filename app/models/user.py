from py2neo import Node, Relationship
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom
from datetime import datetime
import uuid


class User(GraphObject):
    __primarylabel__ = "User"
    __primarykey__ = "id"

    id = Property()
    name = Property()
    email = Property()
    created_at = Property()

    # Relationships
    posts = RelatedFrom("Post", "CREATED")
    comments = RelatedFrom("Comment", "CREATED")
    likes_posts = RelatedTo("Post", "LIKES")
    likes_comments = RelatedTo("Comment", "LIKES")
    friends = RelatedTo("User", "FRIENDS_WITH")

    def __init__(self, name, email):
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.created_at = datetime.now().timestamp()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at,
        }


    @staticmethod
    def find_by_id(user_id, graph):
        result = graph.run(f"MATCH (u:User {{id: '{user_id}'}}) RETURN u").data()
        if result:
            return User.wrap(result[0]["u"])
        return None

    @staticmethod
    def get_all(graph):
        result = graph.run("MATCH (u:User) RETURN u").data()
        return [User.wrap(record["u"]) for record in result]
