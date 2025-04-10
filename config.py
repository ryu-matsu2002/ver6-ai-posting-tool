import os

# 本番環境以外でのみ .env を読み込む
if os.environ.get("FLASK_ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv()

# ベースディレクトリの設定
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # SECRET_KEYを環境変数から取得。なければデフォルトで設定（本番環境では必ず設定すべき）
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret")

    # DATABASE_URL の形式が postgres:// の場合 → SQLAlchemy 用に postgresql:// に修正
    db_url = os.getenv("DATABASE_URL")
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    # Render用にSSLモード強制追加
    if db_url and "sslmode" not in db_url:
        db_url += "?sslmode=require"

    # デフォルトは /tmp にSQLite（Render環境向け）
    if not db_url:
        sqlite_path = os.path.join("/tmp", "app.db")
        db_url = f"sqlite:///{sqlite_path}"

    # SQLAlchemyのデータベースURI設定
    SQLALCHEMY_DATABASE_URI = db_url

    # データベースの変更追跡を無効化（パフォーマンス向上）
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # セッションのクッキー設定（オプション）
    # HTTPSを使用している場合に有効化
    SESSION_COOKIE_SECURE = True if os.environ.get("FLASK_ENV") == "production" else False

    # CSRFの設定（オプション）
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = os.getenv("CSRF_SESSION_KEY", "default_csrf_secret")
