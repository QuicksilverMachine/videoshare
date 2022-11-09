from faker import Faker

from videoshare.models import Folder, Node, NodeType, Video, db

fake = Faker()


class Preconditions:
    def __init__(self):
        self.node = NodePrecondition
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
        video = Video(
            id=id_ or fake.uuid4(),
            name=name or fake.slug(),
            type=NodeType.VIDEO,
            parent_id=parent_id,
        )
        db.session.add(video)
        db.session.commit()
        return video


class FolderPrecondition:
    @staticmethod
    def exists(id_=None, name=None, parent_id=None):
        folder = Folder(
            id=id_ or fake.uuid4(),
            name=name or fake.slug(),
            type=NodeType.FOLDER,
            parent_id=parent_id,
        )
        db.session.add(folder)
        db.session.commit()
        return folder
