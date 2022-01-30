from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from logging import getLogger, StreamHandler, DEBUG
from login_app import app

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class User(Model):
    class Meta:
        table_name = "users"
        region = app.config.get("DYNAMODB_REGION")
        aws_access_key_id = app.config.get("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = app.config.get("AWS_SECRET_ACCESS_KEY")
        host = app.config.get("DYNAMODB_ENDPOINT_URL")

    id = UnicodeAttribute(hash_key=True, null=False)
    password = UnicodeAttribute(null=False)
    name = UnicodeAttribute(null=False)

    def get_id(self):
        logger.debug(f"get_id start")
        return self.id

    def is_authenticated(self):
        logger.debug(f"is_authenticated start")
        return True

    def is_active(self):
        logger.debug(f"is_active start")
        return True

    def is_anonymous(self):
        logger.debug(f"is_anonymous start")
        return False
