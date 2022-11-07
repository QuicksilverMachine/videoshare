from operator import and_, or_
from typing import Any

from flask import Blueprint
from sqlalchemy import select

from videoshare.errors import NotFound
from videoshare.models import Folder, Node

explore_blueprint = Blueprint("explore", __name__, url_prefix="/explore")


@explore_blueprint.route("/")
@explore_blueprint.route("/<path:path>")
def resolve_path(path: str | None = None) -> dict[str, Any]:
    """Resolve path and return list of folders from root to parent"""
    if not path:
        # As path is not specified, using root
        folder_id = None
        folder_name = None
        contents = Node.query.filter(Node.parent_id.is_(None)).all()
    else:
        path_names = path.rstrip("/").split("/")
        root_folder = path_names[0]
        subquery = select(Folder.id).filter(Folder.name == root_folder).subquery()
        for name in path_names[1:]:
            subquery = (
                select(Folder.id)
                .filter(
                    or_(
                        # Get next folder
                        and_(
                            Folder.parent_id.in_(select(subquery)), Folder.name == name
                        ),
                        # And keep current folder
                        Folder.id.in_(select(subquery)),
                    ),
                )
                .subquery()
            )
        folders = Folder.query.filter(Folder.id.in_(select(subquery))).all()

        if not folders or len(folders) != len(path_names):
            raise NotFound("Path could not be resolved")

        # For now, we only take the last folder, previous ones could be
        # used later to display entire path as breadcrumbs
        folder_id = folders[-1].id
        folder_name = folders[-1].name
        contents = Node.query.filter(Node.parent_id == folder_id).all()

    return {
        "id": folder_id,
        "name": folder_name,
        "contents": [
            {
                "id": node.id,
                "name": node.name,
                "type": node.type,
                "parent_id": node.parent_id,
            }
            for node in contents
        ],
    }
