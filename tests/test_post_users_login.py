import pytest
import uuid
from api_helpers import create_user, delete_user, login_user
from common import get_headers


@pytest.fixture
def created_user():
    users_to_delete = []

    def _create_user(task_id, email=None, password="password", name="Elli", nickname="elli"):
        if not email:
            email = f"elli_test_{uuid.uuid4().hex[:8]}@example.com"

        headers = get_headers(task_id=task_id)
        response = create_user(headers, email, password, name, nickname)
        assert response.status_code == 200

        created_data = response.json()
        user_uuid = created_data.get("uuid")
        assert user_uuid

        users_to_delete.append((headers, user_uuid))
        return email, password

    yield _create_user

    for headers, user_uuid in users_to_delete:
        delete_user(headers, user_uuid)


def test_user_login_success_api7(created_user):
    create_task_id = "api-7"
    email, password = created_user(task_id=create_task_id)

    login_task_id = "api-7"
    headers = get_headers(task_id=login_task_id)

    response = login_user(headers, email=email, password=password)

    assert response.status_code == 200
