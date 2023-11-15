import jsonschema
import requests

from utils import load_schema


def test_get_status_code_is_ok():
    response = requests.get(
        url='https://reqres.in/api/users'
    )

    assert response.status_code == 200


def test_get_user_is_found():
    schema = load_schema('get_user.json')

    user_id = 2
    response = requests.get(
        url=f'https://reqres.in/api/users/{user_id}'
    )

    assert response.json()["data"]["id"] == user_id
    jsonschema.validate(response.json(), schema)


def test_get_user_is_not_found():
    response = requests.get(
        url='https://reqres.in/api/users/23'
    )

    assert response.status_code == 404


def test_post_create_user():
    schema = load_schema('post_user.json')

    response = requests.post(
        url='https://reqres.in/api/users',
        json={
            "name": "elena",
            "job": "QA"
        }
    )

    assert response.status_code == 201
    assert response.json()['name'] == "elena"
    jsonschema.validate(response.json(), schema)


def test_put_update_user():
    schema = load_schema('put_user.json')

    response = requests.put(
        url='https://reqres.in/api/users/2',
        json={
            "name": "morpheus",
            "job": "actor"
        }
    )

    assert response.status_code == 200
    assert response.json()['job'] == "actor"
    jsonschema.validate(response.json(), schema)


def test_get_delete_user():
    user_id = 2

    response = requests.delete(
        url=f'https://reqres.in/api/users/{user_id}'
    )

    assert response.status_code == 204


def test_post_successful_registration():
    schema = load_schema('post_register.json')

    response = requests.post(
        url='https://reqres.in/api/register',
        json={
            "email": "eve.holt@reqres.in",
            "password": "pistol"
        }
    )

    assert response.status_code == 200
    jsonschema.validate(response.json(), schema)


def test_post_unsuccessful_registration():
    response = requests.post(
        url='https://reqres.in/api/register',
        json={
            "email": "sydney@fife"
        }
    )

    assert response.status_code == 400
    assert response.json()['error'] == "Missing password"


def test_post_successful_login():
    schema = load_schema('post_login.json')

    response = requests.post(
        url='https://reqres.in/api/login',
        json={
            "email": "eve.holt@reqres.in",
            "password": "cityslicka"
        }
    )

    assert response.status_code == 200
    jsonschema.validate(response.json(), schema)


def test_post_unsuccessful_login():
    response = requests.post(
        url='https://reqres.in/api/login',
        json={
            "email": "peter@klaven"
        }
    )

    assert response.status_code == 400
    assert response.json()['error'] == 'Missing password'
