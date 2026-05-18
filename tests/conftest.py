import pytest
from app import create_app
from app.services import user_service


@pytest.fixture
def client():
    app = create_app()
    return app.test_client()


@pytest.fixture(autouse=True)
def reset_db():
    user_service.users.clear()
    user_service.current_id = 1
