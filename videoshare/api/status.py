from flask import Blueprint

status_blueprint = Blueprint("status", __name__, url_prefix="/status")


@status_blueprint.route("/")
def status() -> dict[str, str]:
    return {"status": "OK"}
