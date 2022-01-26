import pytest

from login_app import app
from logging import getLogger, StreamHandler, DEBUG

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


@pytest.fixture
def client():
    logger.debug("client start")

    with app.test_client() as client:
        yield client


def test_top_not_logined(client):
    rv = client.get("/")
    assert b"Log In" in rv.data


@pytest.fixture(
    params=[
        ("user_id_1", "wrong_password"),
        ("wrong_user_id", "user_id_1_pass"),
        ("", ""),
    ]
)
def login_fail_fixture(request):
    return (request.getfixturevalue("client"), request.param[0], request.param[1])


def test_login_fail(login_fail_fixture):
    client, user_id, password = login_fail_fixture

    # ログインが失敗すると"Login Button"を含む
    rv = login(client, user_id, password)
    assert b"Login Button" in rv.data


def test_top_logined(client):
    # loginが成功するとログイン状態でtopにリダイレクトされるので"Log Out"を含む
    rv = login(client, "user_id_1", "user_id_1_pass")
    assert b"Log Out" in rv.data

    # ログイン状態でtopにアクセスすると"Log Out"を含む
    rv = client.get("/")
    assert b"Log Out" in rv.data


def login(client, user_id, password):
    logger.debug(f"login user_id={user_id} password={password} ")

    return client.post(
        "/login", data=dict(user_id=user_id, password=password), follow_redirects=True
    )
