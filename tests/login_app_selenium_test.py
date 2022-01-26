import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from logging import getLogger, StreamHandler, DEBUG
from tests.test_common import BASE_URL, LOGIN_FORM_URL


logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


@pytest.fixture
def webdriver_chrome() -> webdriver:
    webdriver_chrome = webdriver.Chrome()
    yield webdriver_chrome
    webdriver_chrome.quit()


def test_top_not_logined(webdriver_chrome: webdriver):
    webdriver_chrome.get(BASE_URL)

    login_text = webdriver_chrome.find_element(
        by=By.XPATH, value='//*[contains(., "Log In")]'
    )

    assert not login_text is None


@pytest.fixture(
    params=[
        ("user_id_1", "wrong_password"),
        ("wrong_user_id", "user_id_1_pass"),
        ("", ""),
    ]
)
def login_fail_fixture(request):
    return (
        request.getfixturevalue("webdriver_chrome"),
        request.param[0],
        request.param[1],
    )


def test_login_fail(login_fail_fixture):
    webdriver_chrome, user_id, password = login_fail_fixture

    login(webdriver_chrome, user_id, password)

    # ログインが失敗すると"Login Button"が存在する
    login_button = webdriver_chrome.find_element(by=By.ID, value="LoginButton")
    assert not login_button == None


def login(webdriver_chrome: webdriver, user_id: str, password: str):
    logger.debug(f"login user_id={user_id} password={password} ")

    webdriver_chrome.get(LOGIN_FORM_URL)

    input_user_id = webdriver_chrome.find_element(by=By.ID, value="InputUserId")
    input_user_id.send_keys(user_id)

    input_password = webdriver_chrome.find_element(by=By.ID, value="InputPassword")
    input_password.send_keys(password)

    login_button = webdriver_chrome.find_element(by=By.ID, value="LoginButton")
    login_button.click()


def test_top_logined(webdriver_chrome: webdriver):

    # loginが成功するとログイン状態でtopにリダイレクトされるので"Log Out"を含む
    login(webdriver_chrome, "user_id_1", "user_id_1_pass")

    logout_text = webdriver_chrome.find_element(
        by=By.XPATH, value='//*[contains(., "Log Out")]'
    )
    assert not logout_text == None

    # ログイン状態でtopにアクセスすると"Log Out"を含む
    webdriver_chrome.get(BASE_URL)

    logout_text = webdriver_chrome.find_element(
        by=By.XPATH, value='//*[contains(., "Log Out")]'
    )
    assert not logout_text == None
