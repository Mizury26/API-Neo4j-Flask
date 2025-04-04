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

    def add_friend(self, friend, graph):
        if not isinstance(friend, User):
            raise TypeError("Friend must be a User object")

        relationship = Relationship(self.__node__, "FRIENDS_WITH", friend.__node__)
        graph.create(relationship)
        return relationship

    def remove_friend(self, friend, graph):
        graph.run(
            f"MATCH (u:User {{id: '{self.id}'}})-[r:FRIENDS_WITH]->(f:User {{id: '{friend.id}'}}) DELETE r"
        )

    def is_friend_with(self, friend, graph):
        result = graph.run(
            f"MATCH (u:User {{id: '{self.id}'}})-[:FRIENDS_WITH]->(f:User {{id: '{friend.id}'}}) RETURN f"
        ).data()
        return len(result) > 0

    def get_friends(self, graph):
        result = graph.run(
            f"MATCH (u:User {{id: '{self.id}'}})-[:FRIENDS_WITH]->(f:User) RETURN f"
        ).data()
        return [User.wrap(record["f"]) for record in result]

    def get_mutual_friends(self, other_user, graph):
        query = f"""
        MATCH (u1:User {{id: '{self.id}'}})-[:FRIENDS_WITH]->(mutual:User)<-[:FRIENDS_WITH]-(u2:User {{id: '{other_user.id}'}})
        RETURN mutual
        """
        result = graph.run(query).data()
        return [User.wrap(record["mutual"]) for record in result]

    def like_post(self, post, graph):
        relationship = Relationship(self.__node__, "LIKES", post.__node__)
        graph.create(relationship)
        return relationship

    def unlike_post(self, post, graph):
        graph.run(
            f"MATCH (u:User {{id: '{self.id}'}})-[r:LIKES]->(p:Post {{id: '{post.id}'}}) DELETE r"
        )

    def like_comment(self, comment, graph):
        relationship = Relationship(self.__node__, "LIKES", comment.__node__)
        graph.create(relationship)
        return relationship

    def unlike_comment(self, comment, graph):
        graph.run(
            f"MATCH (u:User {{id: '{self.id}'}})-[r:LIKES]->(c:Comment {{id: '{comment.id}'}}) DELETE r"
        )

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
