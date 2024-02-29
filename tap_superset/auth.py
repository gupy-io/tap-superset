import requests

_TOKEN = None


def get_auth_token(base_url, username, password):
    global _TOKEN
    if _TOKEN is None:
        _TOKEN = fetch_token(base_url, username, password)
    return _TOKEN


def fetch_token(base_url, username, password):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    json_data = {
        "provider": "db",
        "refresh": True,
        "username": username,
        "password": password,
    }

    response = requests.post(
        f"{base_url}/api/v1/security/login",
        headers=headers,
        json=json_data,
    )
    return response.json()["access_token"]
