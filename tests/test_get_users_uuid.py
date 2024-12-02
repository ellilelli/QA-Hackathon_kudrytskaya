import pytest
import uuid
from api_helpers import create_user, delete_user, API_BASE_URL
from common import get_headers
import requests


@pytest.fixture
def created_users():
    users_to_delete = []
    fixture_task_id = "api-23"

    def _create_user(email=None, password="111111", name="Test User", nickname=None):
        if not email:
            email = f"test_{uuid.uuid4().hex[:8]}@example.com"
        if not nickname:
            nickname = f"test_{uuid.uuid4().hex[:8]}"

        headers = get_headers(task_id=fixture_task_id)
        response = create_user(headers, email, password, name, nickname)

        assert response.status_code == 200, f"Expected 200, but got {response.status_code}. Response: {response.text}"

        created_data = response.json()
        user_uuid = created_data.get("uuid")
        assert user_uuid, "User UUID is missing in the response"
        assert len(user_uuid) == 36 and user_uuid.count('-') == 4, f"Invalid UUID format: {user_uuid}"

        users_to_delete.append((headers, user_uuid))
        return headers, user_uuid, email, nickname

    yield _create_user

    for headers, user_uuid in users_to_delete:
        try:
            response = delete_user(headers, user_uuid)

            if response.status_code != 204:
                print(f"Unexpected response during deletion: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error while attempting to delete user with UUID {user_uuid}: {e}")


def test_get_user_by_uuid_api23(created_users):
    fixture_headers, user_uuid_1, email_1, nickname_1 = created_users()
    fixture_headers, user_uuid_2, email_2, nickname_2 = created_users()

    assert user_uuid_1 != user_uuid_2, f"UUIDs should be different: {user_uuid_1} == {user_uuid_2}"

    response = get_user_by_uuid(user_uuid_2)

    assert response.status_code == 200, f"Expected 200, but got {response.status_code}. Response: {response.text}"
    response_data = response.json()

    assert response_data['uuid'] == user_uuid_2, f"Expected UUID {user_uuid_2}, but got {response_data['uuid']}"

    delete_user(fixture_headers, user_uuid_1)
    delete_user(fixture_headers, user_uuid_2)


def get_users(offset=0, limit=2):
    url = f'{API_BASE_URL}/users?offset={offset}&limit={limit}'
    headers = get_headers(task_id="api-23")
    response = requests.get(url, headers=headers)
    return response


def get_user_by_uuid(user_uuid):
    url = f'{API_BASE_URL}/users/{user_uuid}'
    headers = get_headers(task_id="api-23")
    response = requests.get(url, headers=headers)
    return response
