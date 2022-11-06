from typing import Any

from flask import Blueprint

from videoshare.errors import BadRequest, NotFound
from videoshare.models import Folder, Video, db
from videoshare.utils import get_request_json

video_blueprint = Blueprint("video", __name__, url_prefix="/video")


@video_blueprint.route("/", methods=["POST"])
def create() -> dict[str, Any]:
    data = get_request_json()
    name = data.get("name")
    if not name:
        raise BadRequest("Node name is not valid")

    existing = Video.query.filter_by(name=name).first()
    if existing:
        raise BadRequest("Node with that name already exists in folder")

    new_video = Video(name=name)
    db.session.add(new_video)
    db.session.commit()

    return {
        "id": new_video.id,
        "name": new_video.name,
        "type": new_video.type,
        "parent_id": new_video.parent_id,
    }


# noinspection DuplicatedCode
@video_blueprint.route("/<uuid:video_id>", methods=["PATCH"])
def move(video_id: str) -> dict[str, Any]:
    existing = Video.query.filter_by(id=video_id).first()
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
