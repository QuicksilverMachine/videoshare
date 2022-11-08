import pytest

from tests.preconditions import Preconditions
from tests.verifiers import Verifiers
from videoshare.app import create_app
from videoshare.config import TestConfig
from videoshare.models import db


@pytest.fixture(autouse=True, scope="function")
def app():
    app = create_app(configuration=TestConfig)
    app.config.update({})
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    """HTTP client"""
    return app.test_client()


@pytest.fixture()
def runner(app):
    """Cli runner"""
    return app.test_cli_runner()


@pytest.fixture
def given():
    return Preconditions()


@pytest.fixture
def verify():
    return Verifiers()
