import pytest
from pynamodb.exceptions import DoesNotExist

from login_app import app
from login_app.models.users import User
from tests.test_common import request_login


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_login_fail(mocker, client):
    user = User(id="id", password="password")
    mocker.patch.object(User, "get", return_value=user)

    # ログインが失敗すると"Login Button"が存在する
    rv = request_login(client, "id", "wrong_password")
    assert b"Login Button" in rv.data


def test_login_does_not_exist(mocker, client):
    mocker.patch.object(User, "get", side_effect=DoesNotExist)

    # ログインが失敗すると"Login Button"が存在する
    rv = request_login(client, "id", "wrong_password")
    assert b"Login Button" in rv.data


def test_top_logined(mocker, client):
    user = User(id="id", password="password")
    mocker.patch.object(User, "get", return_value=user)

    # loginが成功するとログイン状態でtopにリダイレクトされるので"Log Out"を含む
    rv = request_login(client, user.id, user.password)
    assert b"Log Out" in rv.data

    # ログイン状態でtopにアクセスすると"Log Out"を含む
    rv = client.get("/")
    assert b"Log Out" in rv.data
