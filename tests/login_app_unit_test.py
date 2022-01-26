import pytest

from login_app import app
from login_app.models.users import User


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_login_fail(mocker, client):
    user = User(id="id", password="password")
    mocker.patch.object(User, "get", return_value=user)

    # ログインが失敗すると"Login Button"が存在する
    rv = login(client, "wrong_id", "wrong_password")
    assert b"Login Button" in rv.data


def test_top_logined(mocker, client):
    user = User(id="id", password="password")
    mocker.patch.object(User, "get", return_value=user)

    # loginが成功するとログイン状態でtopにリダイレクトされるので"Log Out"を含む
    rv = login(client, user.id, user.password)
    assert b"Log Out" in rv.data

    # ログイン状態でtopにアクセスすると"Log Out"を含む
    rv = client.get("/")
    assert b"Log Out" in rv.data


def login(client, user_id, password):
    return client.post(
        "/login", data=dict(user_id=user_id, password=password), follow_redirects=True
    )
