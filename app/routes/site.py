# ✅ routes/site.py を新規作成
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Site

site_bp = Blueprint("site", __name__)

@site_bp.route("/site/add", methods=["GET", "POST"])
@login_required
def add_site():
    if request.method == "POST":
        name = request.form["name"]
        url = request.form["url"]
        username = request.form["username"]
        app_password = request.form["app_password"]

        site = Site(
            user_id=current_user.id,
            name=name,
            url=url.rstrip("/"),
            username=username,
            app_password=app_password
        )
        db.session.add(site)
        db.session.commit()
        flash("サイトを登録しました。")
        return redirect(url_for("dashboard.dashboard"))

    return render_template("add_site.html")