# 📁 ファイルパス: app/__init__.py

from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from app.routes.article import article_bp
from app.routes.title import title_bp
from app.routes.keyword import keyword_bp
from app.routes.post_test import post_test_bp
from app.routes.dashboard import dashboard_bp
from app.routes.auto_post import auto_post_bp
from app.routes.admin_log import admin_log_bp
from app.routes.auth import auth_bp  # ← 追加
from app.routes.site import site_bp  # ← この行を追記
from flask_migrate import Migrate
from app.extensions import db

from app.models import User
from app.scheduler import init_scheduler

login_manager = LoginManager()
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    migrate = Migrate(app, db)


    db.init_app(app)
    login_manager.init_app(app)
    init_scheduler(app)

    # Blueprints 登録
    app.register_blueprint(article_bp)
    app.register_blueprint(title_bp)
    app.register_blueprint(keyword_bp)
    app.register_blueprint(post_test_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(auto_post_bp)
    app.register_blueprint(admin_log_bp)
    app.register_blueprint(auth_bp)  # ← 追加
    app.register_blueprint(site_bp)  # ← この行をBlueprint登録部に追加

    @app.route("/")
    def home():
        return redirect(url_for("dashboard.dashboard"))

    return app
