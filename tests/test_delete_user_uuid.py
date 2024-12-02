import pytest
import uuid
from api_helpers import create_user, delete_user
from common import get_headers


@pytest.fixture
def created_user():
    users_to_delete = []
    fixture_task_id = "api-2"

    def _create_user(email=None, password="111111", name="Elli Test", nickname="elli"):
        if not email:
            email = f"elli_test_{uuid.uuid4().hex[:8]}@example.com"

        headers = get_headers(task_id=fixture_task_id)
        response = create_user(headers, email, password, name, nickname)
        assert response.status_code == 200

        created_data = response.json()
        user_uuid = created_data.get("uuid")
        assert user_uuid

        users_to_delete.append((headers, user_uuid))
        return headers, user_uuid

    yield _create_user

    for headers, user_uuid in users_to_delete:
        try:
            response = delete_user(headers, user_uuid)
            if response.status_code != 204:
                print(f"Unexpected response during deletion: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error while attempting to delete user with UUID {user_uuid}: {e}")


def test_user_deleted_api1(created_user):
    fixture_headers, user_uuid = created_user()
    test_task_id = "api-1"
    test_headers = get_headers(task_id=test_task_id)

    response = delete_user(test_headers, user_uuid)
    assert response.status_code == 204
