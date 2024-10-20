import json

import requests



URL = "http://127.0.0.1:8000"

headers = {
    'Content-Type': 'application/json'
}


def api_register(fio: str, username: str, password: str) -> dict:
    url = URL + "/" + "auth/" + "register"

    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(
            {
                "fio": fio,
                "username": username,
                "password": password
            }
        )
    )

    return response.json()


def api_login(username, password) -> dict:
    url = URL + "/" + "auth/" + "login"

    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(
            {
                "username": username,
                "password": password
            }
        )
    )

    return response.json()


def api_all_builds(token: str):
    url = URL + "/" + "builds/" + "all"

    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(
            {
                "key": token
            }
        )
    )

    return response.json()


def api_build(token: str, build_id: int):
    url = URL + "/" + "builds/" + "build"

    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(
            {
                "key": token,
                "id": build_id
            }
        )
    )

    return response.json()


def api_get_components():
    url = URL + "/" + "components/" + "all"

    response = requests.get(
        url=url,
        headers=headers,
    )

    return response.json()


def api_get_clients():
    url = URL + "/" + "clients/" + "all"

    response = requests.get(
        url=url,
        headers=headers,
    )

    return response.json()


def api_create_build(token: str, client: str, components: list):
    url = URL + "/" + "builds/" + "create"

    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(
            {
                "key": token,
                "client": client,
                "components": [{"title": comp} for comp in components]
            }
        )
    )

    return response.json()


def api_all_inc():
    url = URL + "/" + "incidents/" + "all"

    response = requests.get(
        url=url,
        headers=headers
    )

    return response.json()


def api_create_inc(token: str, status: str, topic: str, description: str):
    url = URL + "/" + "incidents/" + "create"

    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(
            {
                "user_id": token,
                "status": status,
                "topic": topic,
                "description": description
            }
        )
    )

    return response.json()


def api_inc(inc_id: str):
    url = URL + "/" + "incidents/" + "incident/" + inc_id

    response = requests.get(
        url=url,
        headers=headers
    )

    return response.json()


def api_edit_inc(incident_id: int, incident_status: str):
    url = URL + "/" + "incidents/" + "edit"

    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(
            {
                "incident_id": incident_id,
                "status": incident_status
            }
        )
    )

    return response.json()


