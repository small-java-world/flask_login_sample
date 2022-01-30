import os
from flask import redirect, url_for, render_template, send_from_directory
from login_app import app

from logging import getLogger, StreamHandler, DEBUG

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

# parameter defaults to ``["GET"]``. ``HEAD`` and
#        ``OPTIONS`` are added automatically.
# だそうです。
@app.route("/")
def top():
    logger.debug("start top")
    return render_template("top.html")


@app.errorhandler(404)
def non_existant_route(error):
    logger.debug("start non_existant_route")
    # 404のときはloginにリダイレクト
    return redirect(url_for("login"))


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static/img"),
        "favicon.ico",
    )
