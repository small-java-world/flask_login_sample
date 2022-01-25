from flask_script import Command
from logging import getLogger, StreamHandler, DEBUG
from login_app.models.sessions import Session
from login_app.models.users import User


logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class InitDB(Command):
    "create database"

    def run(self):
        init_data()


def init_data():
    logger.debug("init_db start")

    if not Session.exists():
        Session.create_table(read_capacity_units=5, write_capacity_units=2)
    if not User.exists():
        User.create_table(read_capacity_units=5, write_capacity_units=2)

    user_1 = User(id="user_id_1", password="user_id_1_pass")
    user_1.save()

    logger.debug("user_id_1.save() end")
