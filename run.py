# 📁 run.py

import os
import sys
from flask_migrate import Migrate
from app import create_app
from app.models import db

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

app = create_app()
migrate = Migrate(app, db)

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(debug=True)
