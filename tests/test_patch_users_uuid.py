import pytest
import uuid
from api_helpers import create_user, delete_user, login_user, patch_user
from common import get_headers


@pytest.fixture
def created_user():
    users_to_delete = []

    def _create_user(task_id, email=None, password="password", name="Elli", nickname=None):
        if not email:
            email = f"elli_test_{uuid.uuid4().hex[:8]}@example.com"
        if not nickname:
            nickname = f"elli_{uuid.uuid4().hex[:8]}"

        headers = get_headers(task_id=task_id)
        response = create_user(headers, email, password, name, nickname)
        assert response.status_code == 200

        created_data = response.json()
        user_uuid = created_data.get("uuid")
        assert user_uuid

        users_to_delete.append((headers, user_uuid))
        return user_uuid, email, password

    yield _create_user

    for headers, user_uuid in users_to_delete:
        delete_user(headers, user_uuid)


def test_patch_user_password_change_api24(created_user):
    task_id = "api-24"
    user_uuid, email, old_password = created_user(task_id=task_id, password="111111")

    new_password = "123456"
    data = {"password": new_password}
    headers = get_headers(task_id=task_id)
    patch_response = patch_user(headers, user_uuid, data)

    assert patch_response.status_code == 200, f"Patch failed: {patch_response.text}"

    login_response = login_user(headers, email=email, password=new_password)
    assert login_response.status_code == 200, f"Login failed: {login_response.text}"
    login_data = login_response.json()
    assert login_data.get("email") == email, f"Expected email {email}, got {login_data.get('email')}"


def test_patch_user_password_duplicate_email_api4(created_user):
    task_id = "api-4"

    user1_uuid, email1, _ = created_user(task_id=task_id)
    user2_uuid, email2, _ = created_user(task_id=task_id)

    data = {"email": email2}
    headers = get_headers(task_id=task_id)
    patch_response = patch_user(headers, user1_uuid, data)

    assert patch_response.status_code == 409, (
        f"Expected 409 Conflict, but got {patch_response.status_code}: {patch_response.text}"
    )
