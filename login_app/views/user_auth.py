from flask import request, redirect, url_for, render_template, flash, session
from flask_login import login_user, logout_user, login_required

from logging import getLogger, StreamHandler, DEBUG
from pynamodb.exceptions import DoesNotExist
from login_app import app


logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


@app.route("/login", methods=["GET", "POST"])
def login():
    logger.debug("login start")

    # 以前にflashした値をクリア
    session.pop("_flashes", None)

    if request.method == "POST":
        user_id = request.form["user_id"]
        password = request.form["password"]

        if user_id:
            try:
                from login_app.models.users import User

                user = User.get(user_id)

                if user.password != password:
                    logger.error(f"パスワードが一致しません。")

                    flash("ユーザーIDもしくはパスワードが不正です。")
                else:
                    logger.debug(f"login成功 id={user.id}")

                    login_user(user)

                    logger.debug(f"call login_user end")

                    flash("ログインしました。")

                    return redirect(url_for("top"))
            except DoesNotExist:
                flash("ユーザーIDもしくはパスワードが不正です。")
                logger.error(f"ユーザが存在しません。user_id={user_id}")
        else:
            flash("ユーザーIDが指定されていません。")

    return render_template("login.html")


@app.route("/logout")
def logout():
    logger.debug("logout start")

    logout_user()
    flash("ログアウトしました。")
    return redirect(url_for("login"))


@app.route("/users/detail/<user_id>", methods=["GET"])
@login_required
def user_detail(user_id):
    logger.debug(f"user_detail user_id={user_id} start")

    try:
        from login_app.models.users import User

        user = User.get(user_id)
        return render_template("user_detail.html", user=user)

    except DoesNotExist:
        flash("ユーザが存在しません。")
        logger.error(f"user_detail ユーザが存在しません。user_id={user_id}")

        return redirect(url_for("top"))
