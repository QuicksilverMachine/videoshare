import uuid

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.util import classproperty

db = SQLAlchemy()
migrate = Migrate()


class NodeType:
    FOLDER = "folder"
    FILE = "file"
    VIDEO = "video"


class Node(db.Model):  # type: ignore
    __tablename__ = "nodes"

    id = db.Column(UUID, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    parent_id = db.Column(UUID, db.ForeignKey("nodes.id"))

    # Index both nullable and non-nullable parent id to cover the case
    # of root folder being NULL, since NULL is not comparable in SQL by design
    __table_args__ = (
        Index(
            "uix_unique_name_type_parent_id",
            "name",
            "type",
            "parent_id",
            unique=True,
            postgresql_where=parent_id.isnot(None),
        ),
        Index(
            "uix_unique_name_type_parent_id_null",
            "name",
            "type",
            "parent_id",
            unique=True,
            postgresql_where=parent_id.is_(None),
        ),
    )

    # noinspection PyMethodParameters
    @classproperty
    def __mapper_args__(cls) -> dict[str, str]:
        """Maps nodes to specific models based on type"""
        return dict(
            polymorphic_on="type",
            polymorphic_identity=cls.__name__.lower(),
            with_polymorphic="*",
        )

    def __repr__(self) -> str:
        return f"<Node {self.type} {self.name}>"


class Folder(Node):
    children = db.relationship(
        "Node", backref=db.backref("parent", remote_side=[Node.id])
    )

    def __repr__(self) -> str:
        return f"<Folder {self.name}>"


class File(Node):
    def __repr__(self) -> str:
        return f"<File {self.name}>"


class Video(File):
    def __repr__(self) -> str:
        return f"<Video {self.name}>"
