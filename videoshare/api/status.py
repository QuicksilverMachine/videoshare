from apiflask import APIBlueprint

from videoshare.schema.response import StatusResponse

status_blueprint = APIBlueprint("status", __name__, url_prefix="/status")


@status_blueprint.route("/")
@status_blueprint.output(StatusResponse)
def status() -> dict[str, str]:
    """Return OK as a health-check signal"""
    return {"status": "OK"}
