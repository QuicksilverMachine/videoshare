from typing import Any

from flask import Blueprint

explore_blueprint = Blueprint("explore", __name__, url_prefix="/explore")


@explore_blueprint.route("/")
def get() -> dict[str, Any]:
    return {}
