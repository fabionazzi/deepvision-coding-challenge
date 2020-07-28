from app import app
from flask import json
import base64


# Credentials for authentication test
valid_credentials = base64.b64encode(b"user1:pass1").decode("utf-8")
invalid_credentials = base64.b64encode(b"user1:pass4").decode("utf-8")
valid_token = ''

def test_valid_login():
    global valid_token
    response = app.test_client().get(
        '/login',
        headers = {
            "Authorization": "Basic {}".format(valid_credentials)
        }
    )
    valid_token = json.loads(response.get_data())['token']
    assert response.status_code == 200


def test_invalid_login():
    response = app.test_client().get(
        '/login',
        headers={
            "Authorization": "Basic {}".format(invalid_credentials)
        }
    )
    assert response.status_code == 401


valid_query = '?day=2015-09-06'
def test_get_efemerides_with_valid_date():
    response = app.test_client().get(
        '/efemerides{}'.format(valid_query),
        headers={
            'Content-Type': 'application/json',
            'x-access-token': valid_token
        }
    )
    assert response.status_code == 200


invalid_query_args = '?day=2015-20-06'
def test_get_efemerides_with_invalid_query_args():
    response = app.test_client().get(
        '/efemerides{}'.format(invalid_query_args),
        headers={
            'Content-Type': 'application/json',
            'x-access-token': valid_token
        }
    )
    assert response.status_code == 400


invalid_query_key = '?dummy=2015-20-06'
def test_get_efemerides_with_invalid_query_key():
    response = app.test_client().get(
        '/efemerides{}'.format(invalid_query_args),
        headers={
            'Content-Type': 'application/json',
            'x-access-token': valid_token
        }
    )
    assert response.status_code == 400


def test_invalid_method_post():
    response = app.test_client().post(
        '/efemerides',
    )
    assert response.status_code == 405 


def test_invalid_method_put():
    response = app.test_client().put(
        '/efemerides',
    )
    assert response.status_code == 405 


def test_invalid_method_delete():
    response = app.test_client().post(
        '/efemerides',
    )
    assert response.status_code == 405 