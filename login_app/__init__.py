import os
from flask import session
from flask import Flask
from flask_login import LoginManager
from flask_sessionstore import Session
from logging import getLogger, StreamHandler, DEBUG

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


app = Flask(__name__, instance_relative_config=True)

# 各種設定の読み込み
try:
    run_flag = os.environ["RUN_FLAG"]
except KeyError:
    run_flag = "1"

config_name = "login_app.config.DevConfig"

"""
RuntimeError: The table sessions does not exist in DynamoDB for the requested region・・・
と怒られるのでmanage_db.pyの呼び出しの時はDevDbInitConfig or TestDbInitConfigにして
SESSION_TYPE = ""としセッション機能を無効にする。
"""
if run_flag == "1":
    config_name = "login_app.config.DevConfig"
elif run_flag == "2":
    config_name = "login_app.config.TestConfig"
elif run_flag == "3":
    config_name = "login_app.config.DevDbInitConfig"
elif run_flag == "4":
    config_name = "login_app.config.TestDbInitConfig"

logger.debug(f"run_flag={run_flag} config_name={config_name}")

app.config.from_object(config_name)

# user_auth, commonをimportしないとルーティングされない
from login_app.views import user_auth, common

# セッション管理を有効化
Session(app)

# flask_loginの初期化
login_manager = LoginManager()
login_manager.init_app(app)

from login_app.user_loader import setup_auth

# userをロードするためのcallbackを定義
setup_auth(login_manager)

# @login_requiredが付与されたurlにアクセスし、未ログインの場合はここにリダイレクトされる。
login_manager.login_view = "login"
login_manager.login_message = "ログインしてください"
