import requests
from common import API_BASE_URL


def create_user(headers, email, password, name, nickname):
    url = f"{API_BASE_URL}/users"
    data = {
        "email": email,
        "password": password,
        "name": name,
        "nickname": nickname
    }
    response = requests.post(url, json=data, headers=headers)
    return response


def get_user(headers, user_uuid):
    url = f"{API_BASE_URL}/users/{user_uuid}"
    response = requests.get(url, headers=headers)
    return response


def delete_user(headers, user_uuid):
    url = f"{API_BASE_URL}/users/{user_uuid}"
    response = requests.delete(url, headers=headers)

    if response.status_code not in [200, 204]:
        raise Exception(f"Failed to delete user: {response.status_code} - {response.text}")
    return response


def login_user(headers, email, password):
    url = f"{API_BASE_URL}/users/login"
    payload = {"email": email, "password": password}
    response = requests.post(url, json=payload, headers=headers)
    return response


def patch_user(headers, user_uuid, data):
    url = f"{API_BASE_URL}/users/{user_uuid}"
    response = requests.patch(url, headers=headers, json=data)
    return response
