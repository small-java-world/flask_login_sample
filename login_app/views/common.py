from flask import redirect, url_for, render_template
from login_app import app

from logging import getLogger, StreamHandler, DEBUG

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


@app.route("/")
def top():
    logger.debug("start top")
    return render_template("top.html")


@app.errorhandler(404)
def non_existant_route(error):
    logger.debug("start non_existant_route")
    return redirect(url_for("login"))
