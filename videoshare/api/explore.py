from typing import Any

from flask import Blueprint

from videoshare.errors import BadRequest
from videoshare.models import Folder

explore_blueprint = Blueprint("explore", __name__, url_prefix="/explore")


@explore_blueprint.route("/<path:path>")
def resolve_path(path: str) -> dict[str, Any]:
    """Resolve path and return list of folders from root to parent"""

    if not path:
        raise BadRequest("Invalid path provided")

    folder = Folder.query.filter_by(path=path).first()
    if not folder:
        raise BadRequest("Path is not a folder or does not exist")

    return {
        "id": folder.id,
        "name": folder.name,
        "parent_id": folder.parent_id,
        "type": folder.type,
    }
