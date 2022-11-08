from apiflask import APIBlueprint

status_blueprint = APIBlueprint("status", __name__, url_prefix="/status")


@status_blueprint.route("/")
def status() -> dict[str, str]:
    return {"status": "OK"}
