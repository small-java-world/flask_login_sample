from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from login_app import app


class User(Model):
    class Meta:
        table_name = "users"
        region = app.config.get("DYNAMODB_REGION")
        aws_access_key_id = app.config.get("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = app.config.get("AWS_SECRET_ACCESS_KEY")
        host = app.config.get("DYNAMODB_ENDPOINT_URL")

    id = UnicodeAttribute(hash_key=True, null=False)
    password = UnicodeAttribute(null=False)

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False
