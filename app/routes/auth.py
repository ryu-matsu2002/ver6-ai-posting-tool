# 📁 ファイルパス: app/routes/auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("ユーザー名またはパスワードが正しくありません。", "error")
            return render_template("login.html")

        login_user(user)
        return redirect(url_for("dashboard.dashboard"))

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if User.query.filter_by(email=email).first():
            flash("このメールアドレスは既に登録されています。", "error")
            return render_template("register.html")

        new_user = User(
            username=username,
            email=email,
            password = generate_password_hash(password, method="pbkdf2:sha256")

        )
        db.session.add(new_user)
        db.session.commit()
        flash("新規登録が完了しました。ログインしてください。", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")
