from typing import Type

from flask import Flask

from videoshare.cli import dev_cli
from videoshare.config import Config
from videoshare.errors import register_error_handlers


def create_app(configuration: Type[Config] = Config) -> Flask:
    """Initialize the core application."""
    app = Flask(__name__)
    app.config.from_object(configuration)

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
