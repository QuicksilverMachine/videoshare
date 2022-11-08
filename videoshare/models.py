import logging
import uuid

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql.psycopg2 import PGExecutionContext_psycopg2
from sqlalchemy.util import classproperty

db = SQLAlchemy()
migrate = Migrate()
logger = logging.getLogger(__name__)


class NodeType:
    FOLDER = "folder"
    FILE = "file"
    VIDEO = "video"


def get_path(name: str, parent_id: str) -> str:
    if not parent_id:
        return f"{name}"
    parent = Node.query.filter_by(id=parent_id).first()
    return f"{parent.path}/{name}"


def default_node_path(context: PGExecutionContext_psycopg2) -> str:
    current_parameters = context.get_current_parameters()
    name = current_parameters.get("name")
    parent_id = current_parameters.get("parent_id")
    logger.debug("Updating path for node %s", current_parameters.get("id"))

    return get_path(name=name, parent_id=parent_id)


def on_update_node_path(context: PGExecutionContext_psycopg2) -> None:
    node_id = str(context.get_current_parameters().get("nodes_id"))
    logger.debug("Updating path for node %s", node_id)
    node = Node.query.filter_by(id=node_id).first()
    node_path = get_path(name=node.name, parent_id=node.parent_id)

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
        default=default_node_path,
        onupdate=on_update_node_path,
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

    def update_children_paths(self) -> None:
        """Recursively discover all children and update their paths"""
        logger.debug("Updating child node paths for node %s", self.id)
        beginning_getter = Node.query.filter(Node.id == self.id).cte(
            name="children_for", recursive=True
        )
        with_recursive = beginning_getter.union_all(
            Node.query.filter(Node.parent_id == beginning_getter.c.id)
        )
        result = db.session.query(with_recursive).all()
        for row in result:
            node = Node.query.filter_by(id=row[0]).first()
            node.path = get_path(name=row[1], parent_id=row[3])
            db.session.add(node)


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
