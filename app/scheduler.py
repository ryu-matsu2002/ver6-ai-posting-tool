# 📁 ファイルパス: app/scheduler.py

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from app.models import db, ScheduledPost
from app.utils.wordpress_post import post_to_wordpress
from app.extensions import db

scheduler = BackgroundScheduler()
scheduler_app = None  # Flaskアプリとの連携用

def check_and_post():
    if scheduler_app is None:
        print("⚠️ scheduler_app is None。Flaskアプリとの連携に失敗しています。")
        return

    with scheduler_app.app_context():
        now = datetime.utcnow()

        # ✅ 1回の実行でランダムに3件だけ投稿
        posts = ScheduledPost.query.filter(
            ScheduledPost.scheduled_time <= now,
            ScheduledPost.posted == False
        ).order_by(db.func.random()).limit(3).all()

        for post in posts:
            success, msg = post_to_wordpress(
                post.site_url,
                post.username,
                post.app_password,
                post.title,
                post.body,
                post.featured_image
            )

            if success:
                post.posted = True
                db.session.commit()
                print(f"✅ 投稿完了: {post.title}")
            else:
                print(f"❌ 投稿失敗: {post.title} | エラー: {msg}")

# ✅ 1分おきにチェックするジョブを登録
scheduler.add_job(func=check_and_post, trigger="interval", minutes=1)
scheduler.start()

def init_scheduler(app):
    global scheduler_app
    scheduler_app = app
