from typing import Any

from flask import Blueprint

from videoshare.errors import NotFound
from videoshare.models import Folder, Node

explore_blueprint = Blueprint("explore", __name__, url_prefix="/explore")


@explore_blueprint.route("/")
@explore_blueprint.route("/<path:path>")
def resolve_path(path: str | None = None) -> dict[str, Any]:
    """Resolve path and return list of folders from root to parent"""
    if not path:
        # As path is not specified, using root
        folder = Folder(id=None, name=None, parent_id=None)
        contents = Node.query.filter(Node.parent_id.is_(None)).all()
    else:
        path = path.strip("/")
        folder = Folder.query.filter_by(path=path).first()
        if not folder:
            raise NotFound("Path could not be resolved")
        contents = folder.children

    return {
        "path": path,
        "id": folder.id,
        "name": folder.name,
        "parent_id": folder.parent_id,
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
