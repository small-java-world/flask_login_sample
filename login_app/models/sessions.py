from datetime import datetime
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute
from login_app import app


class Session(Model):
    class Meta:
        table_name = "sessions"
        region = app.config.get("DYNAMODB_REGION")
        aws_access_key_id = app.config.get("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = app.config.get("AWS_SECRET_ACCESS_KEY")
        host = app.config.get("DYNAMODB_ENDPOINT_URL")

    SessionId = UnicodeAttribute(hash_key=True, null=False)
    Session = UnicodeAttribute(null=True)
