import os


class Config(object):
    DEBUG = True

    # AWS_ACCESS_KEY_ID ローカルなのでなんでもOK
    AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID_DUMMY"
    # AWS_SECRET_ACCESS_KEY ローカルなのでなんでもOK
    AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY_DUMMY"

    SECRET_KEY = "secret key dummy"
    USERNAME = "dummy_user"
    PASSWORD = "dummy_pass"

    # session情報をdynamodbに保存
    SESSION_TYPE = "dynamodb"
    SESSION_DYNAMODB_TABLE = "sessions"


class DevConfig(Config):
    # dynamodb_localのURL
    DYNAMODB_ENDPOINT_URL = "http://localhost:8000"

    # この設定ないとAWSに接続しにいく
    SESSION_DYNAMODB_ENDPOINT_URL = DYNAMODB_ENDPOINT_URL


class TestConfig(Config):
    # dynamodb_localのURL
    DYNAMODB_ENDPOINT_URL = "http://localhost:9000"

    # この設定ないとAWSに接続しにいく
    SESSION_DYNAMODB_ENDPOINT_URL = DYNAMODB_ENDPOINT_URL


class DevDbInitConfig(DevConfig):
    SESSION_TYPE = ""


class TestDbInitConfig(TestConfig):
    SESSION_TYPE = ""
