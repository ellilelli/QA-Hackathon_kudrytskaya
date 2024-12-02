import pytest
import uuid
from api_helpers import create_user, get_user, delete_user
from common import get_headers


@pytest.fixture
def created_user():
    users_to_delete = []

    def _create_user(task_id, email=None, password="111111", name="Elli Test", nickname="elli"):
        if not email:
            email = f"elli_test_{uuid.uuid4().hex[:8]}@example.com"

        headers = get_headers(task_id=task_id)
        response = create_user(headers, email, password, name, nickname)
        assert response.status_code == 200

        created_data = response.json()
        user_uuid = created_data.get("uuid")
        assert user_uuid

        users_to_delete.append((headers, user_uuid))
        return str(user_uuid), response

    yield _create_user

    for headers, user_uuid in users_to_delete:
        delete_user(headers, user_uuid)


def test_set_nickname_api3(created_user):
    task_id = "api-3"

    user_uuid, response = created_user(task_id=task_id)
    headers = get_headers(task_id=task_id)

    response = get_user(headers, user_uuid)
    user_data = response.json()

    assert user_data.get('nickname') == "elli"


def test_create_user_with_numeric_name_api22(created_user):
    task_id = "api-22"

    email = f"elli_numeric_{uuid.uuid4().hex[:8]}@example.com"
    name = "121"
    nickname = "elli_test_numeric"

    user_uuid, response = created_user(task_id=task_id, email=email, name=name, nickname=nickname)

    assert response.status_code == 200
