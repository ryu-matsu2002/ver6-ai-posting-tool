# 📁 ファイルパス: app/models.py

from datetime import datetime
from flask_login import UserMixin
from app.extensions import db  # ここからのみ db を使用する（再定義しない）

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(200), nullable=False)

    posts = db.relationship("ScheduledPost", backref="user", lazy=True)


class ScheduledPost(db.Model):
    __tablename__ = "scheduled_posts"

    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(100), nullable=False)
    keyword = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(300), nullable=False)
    body = db.Column(db.Text, nullable=False)
    featured_image = db.Column(db.String(500), nullable=True)
    site_url = db.Column(db.String(300), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    app_password = db.Column(db.String(100), nullable=False)
    scheduled_time = db.Column(db.DateTime, nullable=False)
    posted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    site_id = db.Column(db.Integer)

    def __repr__(self):
        return f"<ScheduledPost {self.title[:20]} | {self.scheduled_time}>"


class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    app_password = db.Column(db.String(255), nullable=False)

    user = db.relationship("User", backref=db.backref("sites", lazy=True))
