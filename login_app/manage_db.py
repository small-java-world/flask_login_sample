from flask_script import Manager
from login_app import app
from login_app.scripts.init_db import InitDB


if __name__ == "__main__":
    manager = Manager(app)
    manager.add_command("init_db", InitDB())
    manager.run()
