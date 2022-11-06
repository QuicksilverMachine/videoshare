import uuid

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql.psycopg2 import PGExecutionContext_psycopg2
from sqlalchemy.util import classproperty

db = SQLAlchemy()
migrate = Migrate()


class NodeType:
    FOLDER = "folder"
    FILE = "file"
    VIDEO = "video"


def get_node_path(
    context: PGExecutionContext_psycopg2, node_id: str | None = None
) -> str:
    """Context-sensitive function for determining node path"""
    current_parameters = context.get_current_parameters()

    # Get node name from current parameters if it's new
    # or from model if it already exists
    if not node_id:
        name = current_parameters.get("name")
    else:
        node = Node.query.filter_by(id=node_id).first()
        name = node.name

    # Get parent if exists, otherwise use root folder
    parent_id = current_parameters.get("parent_id")
    if not parent_id:
        return f"{name}"
    parent = Node.query.filter_by(id=parent_id).first()
    return f"{parent.path}/{name}"


def set_node_path(context: PGExecutionContext_psycopg2) -> None:
    """Context-sensitive function for setting node path"""
    node_id = str(context.get_current_parameters().get("nodes_id"))
    node_path = get_node_path(context=context, node_id=node_id)

    # Set path based on new parent
    context.current_parameters["path"] = node_path


class Node(db.Model):  # type: ignore
    __tablename__ = "nodes"
    NODE_TYPE: str | None = None

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False, default=NODE_TYPE)
    parent_id = db.Column(UUID(as_uuid=True), db.ForeignKey("nodes.id"), nullable=True)
    path = db.Column(
        db.String,
        nullable=False,
        index=True,
        default=get_node_path,
        onupdate=set_node_path,
    )

    # Index both nullable and non-nullable parent id to cover the case
    # of root folder being NULL, since NULL is not comparable in SQL by design
    __table_args__ = (
        Index(
            "uix_unique_name_type_parent_id",
            name,
            parent_id,
            unique=True,
            postgresql_where=parent_id.isnot(None),
        ),
        Index(
            "uix_unique_name_type_parent_id_null",
            name,
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
    NODE_TYPE = NodeType.FOLDER

    children = db.relationship(
        "Node", backref=db.backref("parent", remote_side=[Node.id])
    )

    def __repr__(self) -> str:
        return f"<Folder {self.name}>"


class File(Node):
    NODE_TYPE = NodeType.FILE

    def __repr__(self) -> str:
        return f"<File {self.name}>"


class Video(File):
    NODE_TYPE = NodeType.VIDEO

    def __repr__(self) -> str:
        return f"<Video {self.name}>"
