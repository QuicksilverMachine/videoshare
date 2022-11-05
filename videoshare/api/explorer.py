from typing import Any

from flask import Blueprint

explorer_blueprint = Blueprint("explorer", __name__, url_prefix="/explorer")


@explorer_blueprint.route("/")
def get() -> dict[str, Any]:
    return {}
