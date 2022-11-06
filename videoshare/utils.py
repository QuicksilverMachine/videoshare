from typing import Any

from flask import request

from videoshare.errors import BadRequest


def get_request_json() -> dict[str, Any]:
    if not request.json or not isinstance(request.json, dict):
        raise BadRequest("Invalid JSON data")
    return request.json
