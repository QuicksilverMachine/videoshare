from typing import Type

from flask import Flask

from videoshare.config import Config


def create_app(configuration: Type[Config] = Config) -> Flask:
    """Initialize the core application."""
    app = Flask(__name__)
    app.config.from_object(configuration)

    # Prepare database
    from videoshare.models import db, migrate

    db.init_app(app=app)
    migrate.init_app(app, db)

    with app.app_context():
        from videoshare.api import routes

        # Register all blueprints
        for route in routes:
            app.register_blueprint(blueprint=route)

        return app
