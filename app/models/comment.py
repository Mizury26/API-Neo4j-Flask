from py2neo.ogm import GraphObject, Property, RelatedFrom
from datetime import datetime
import uuid

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

    @staticmethod
    def find_by_id(graph, comment_id):
        result = graph.evaluate("MATCH (c:Comment {id: $id}) RETURN c", id=comment_id)
        return Comment.wrap(result) if result else None

    @staticmethod
    def get_all(graph):
        result = graph.run("MATCH (c:Comment) RETURN c").data()
        return [Comment.wrap(record['c']) for record in result]

    @staticmethod
    def get_by_post(graph, post_id):
        result = graph.run("MATCH (p:Post {id: $post_id})-[:HAS_COMMENT]->(c:Comment) RETURN c", post_id=post_id).data()
        return [Comment.wrap(record['c']) for record in result]