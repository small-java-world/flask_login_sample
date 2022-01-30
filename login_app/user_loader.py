from logging import getLogger, StreamHandler, DEBUG

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


def setup_auth(login_manager):
    @login_manager.user_loader
    def load_user(user_id):
        logger.debug(f"load_user user_id={user_id}")
        from login_app.models.users import User

        return User(user_id)
    