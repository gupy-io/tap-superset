import requests


def get_auth_token(base_url, username, password):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    json_data = {
        "provider": "db",
        "refresh": False,
        "username": username,
        "password": password,
    }

    response = requests.post(
        f"{base_url}/api/v1/security/login",
        headers=headers,
        json=json_data,
    )
    return response.json()["access_token"]
