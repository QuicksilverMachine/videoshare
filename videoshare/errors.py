from typing import Any

from flask import Flask, json
from werkzeug import exceptions


def register_error_handlers(app: Flask) -> None:
    app.register_error_handler(exceptions.HTTPException, handle_exception)


def handle_exception(e: exceptions.HTTPException) -> Any:
    """Return JSON instead of HTML for HTTP errors."""
    # Start with the correct headers and status code from the error
    response = e.get_response()

    # Replace the body with JSON
    response.data = json.dumps(  # type: ignore
        {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return response


class NotFound(exceptions.NotFound):
    pass


class BadRequest(exceptions.BadRequest):
    pass
