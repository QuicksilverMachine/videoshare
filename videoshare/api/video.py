from typing import Any

from apiflask import APIBlueprint

from videoshare.errors import BadRequest, NotFound
from videoshare.models import Folder, Node, Video, db
from videoshare.utils import get_request_json

video_blueprint = APIBlueprint("video", __name__, url_prefix="/video")


@video_blueprint.route("/", methods=["POST"])
def create() -> dict[str, Any]:
    # noinspection DuplicatedCode
    data = get_request_json()
    name = data.get("name")
    parent_id = data.get("parent_id")

    if not name:
        raise BadRequest("Node name is not valid")

    existing = Video.query.filter_by(name=name, parent_id=parent_id).first()
    if existing:
        raise BadRequest("Node with that name already exists in folder")

    if parent_id:
        parent = Folder.query.filter_by(id=parent_id).first()
        if not parent:
            raise BadRequest("Parent does not exist or is not a folder")

    new_video = Video(name=name, parent_id=parent_id)
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
        if any([existing.name in [child.name for child in new_parent.children]]):
            raise BadRequest("New parent already contains a node with the same name")
    else:
        if any(
            [
                existing.name == child.name and existing.parent_id is not None
                for child in Node.query.filter(
                    Node.name == existing.name, Node.parent_id.is_(None)
                )
            ]
        ):
            raise BadRequest("Root already contains a node with the same name")

    existing.parent_id = new_parent_id
    db.session.add(existing)
    db.session.flush()

    # Update children's paths
    existing.update_children_paths()
    db.session.commit()

    return {
        "id": existing.id,
        "name": existing.name,
        "type": existing.type,
        "parent_id": existing.parent_id,
    }
