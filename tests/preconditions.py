from faker import Faker

from videoshare.models import Node, NodeType, db

fake = Faker()


class Preconditions:
    def __init__(self):
        self.video = VideoPrecondition
        self.folder = FolderPrecondition


class NodePrecondition:
    @staticmethod
    def exists(id_=None, name=None, type_=None, parent_id=None):
        node = Node(
            id=id_ or fake.uuid4(),
            name=name or fake.slug(),
            type=type_,
            parent_id=parent_id,
        )
        db.session.add(node)
        db.session.commit()
        return node


class VideoPrecondition:
    @staticmethod
    def exists(id_=None, name=None, parent_id=None):
        return NodePrecondition.exists(
            id_=id_, name=name, type_=NodeType.VIDEO, parent_id=parent_id
        )


class FolderPrecondition:
    @staticmethod
    def exists(id_=None, name=None, parent_id=None):
        return NodePrecondition.exists(
            id_=id_, name=name, type_=NodeType.FOLDER, parent_id=parent_id
        )
