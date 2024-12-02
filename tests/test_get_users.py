import requests
import pytest
from common import get_headers, API_BASE_URL


@pytest.fixture
def headers():
    return get_headers()


@pytest.fixture
def initial_users(headers):
    response = requests.get(f"{API_BASE_URL}/users?limit=2", headers=headers)
    assert response.status_code == 200
    users = response.json().get('users', [])
    assert len(users) == 2
    return users


def test_offset_non_zero_api6():
    headers = get_headers(task_id="api-6")

    response = requests.get(f"{API_BASE_URL}/users?limit=2", headers=headers)
    assert response.status_code == 200
    users = response.json().get('users', [])
    assert len(users) == 2

    expected_user = users[1]

    response = requests.get(f"{API_BASE_URL}/users?offset=1&limit=1", headers=headers)
    assert response.status_code == 200
    users = response.json().get('users', [])
    assert len(users) == 1

    returned_user = users[0]
    assert returned_user == expected_user


def test_total_count_api21():
    headers = get_headers(task_id="api-21")

    response = requests.get(f"{API_BASE_URL}/users?limit=100", headers=headers)
    assert response.status_code == 200
    data = response.json()
    users = data.get('users', [])
    total = data.get('meta', {}).get('total', 0)

    actual_user_count = len(users)
    assert total == actual_user_count
