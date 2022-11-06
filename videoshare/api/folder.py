from typing import Any

from flask import Blueprint

from videoshare.errors import BadRequest, NotFound
from videoshare.models import Folder, db
from videoshare.utils import get_request_json

folder_blueprint = Blueprint("folder", __name__, url_prefix="/folder")


@folder_blueprint.route("/<uuid:folder_id>")
def get(folder_id: str) -> dict[str, Any]:
    folder = Folder.query.filter_by(id=folder_id).first()
    if folder is None:
        raise NotFound()

    return {
        "name": folder.name,
        "children": [
            {
                "id": child.id,
                "name": child.name,
                "type": child.type,
            }
            for child in folder.children
        ],
    }


@folder_blueprint.route("/", methods=["POST"])
def create() -> dict[str, Any]:
    data = get_request_json()
    name = data.get("name")
    if not name:
        raise BadRequest("Node name is not valid")

    existing = Folder.query.filter_by(name=name).first()
    if existing:
        raise BadRequest("Node with that name already exists in folder")

    new_folder = Folder(name=name)
    db.session.add(new_folder)
    db.session.commit()

    return {
        "id": new_folder.id,
        "name": new_folder.name,
        "type": new_folder.type,
        "parent_id": new_folder.parent_id,
    }


# noinspection DuplicatedCode
@folder_blueprint.route("/<uuid:folder_id>", methods=["PATCH"])
def move(folder_id: str) -> dict[str, Any]:
    existing = Folder.query.filter_by(id=folder_id).first()
    if not existing:
        raise NotFound("Node with that id does not exist")

    data = get_request_json()
    new_parent_id = data.get("parent_id")
    if new_parent_id:
        new_parent = Folder.query.filter_by(id=new_parent_id).first()
        if not new_parent:
            raise BadRequest("New parent does not exist or is not a folder")

    existing.parent_id = new_parent_id
    db.session.add(existing)
    db.session.commit()

    return {
        "id": existing.id,
        "name": existing.name,
        "type": existing.type,
        "parent_id": existing.parent_id,
    }
