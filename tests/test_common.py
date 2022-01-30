from logging import getLogger, StreamHandler, DEBUG

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

BASE_URL = "http:\\localhost:5000"
LOGIN_FORM_URL = f"{BASE_URL}/login"


def request_login(client, user_id, password):
    logger.debug(f"request_login user_id={user_id} password={password} ")

    return client.post(
        "/login", data=dict(user_id=user_id, password=password), follow_redirects=True
    )


def request_user_detail(client, user_id):
    logger.debug(f"request_user_detail user_id={user_id}")

    return client.get(
        f"/users/detail/{user_id}",
        follow_redirects=True,
    )
