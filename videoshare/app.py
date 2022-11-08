from typing import Type

from apiflask import APIFlask
from flask import Flask
from flask_cors import CORS

from videoshare.cli import dev_cli
from videoshare.config import Config
from videoshare.errors import register_error_handlers
from videoshare.version import __version__


def create_app(configuration: Type[Config] = Config) -> Flask:
    """Initialize the core application."""
    app = APIFlask(__name__, title="Videoshare API", version=__version__)
    app.config.from_object(configuration)

    # Set CORS headers
    CORS(app=app)

    # Prepare database
    from videoshare.models import db, migrate

    db.init_app(app=app)
    migrate.init_app(app, db)

    # Initialize custom dev commands
    app.cli.add_command(dev_cli)

    # Register all error handlers
    register_error_handlers(app=app)

    with app.app_context():
        from videoshare.api import routes

        # Register all blueprints
        for route in routes:
            app.register_blueprint(blueprint=route)

        return app
