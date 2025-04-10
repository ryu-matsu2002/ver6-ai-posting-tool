from flask import Blueprint, render_template, request
from app.utils.wordpress_post import post_to_wordpress
from app.extensions import db

post_test_bp = Blueprint("post_test", __name__)

@post_test_bp.route("/post-test", methods=["GET", "POST"])
def post_test():
    result = None

    if request.method == "POST":
        site_url = request.form.get("site_url")
        username = request.form.get("username")
        app_password = request.form.get("app_password")
        title = request.form.get("title")
        content = request.form.get("content")
        image_url = request.form.get("image_url")

        success, message = post_to_wordpress(
            site_url.strip(), username.strip(), app_password.strip(),
            title.strip(), content.strip(), image_url.strip()
        )

        result = {
            "success": success,
            "message": message
        }

    return render_template("post_test.html", result=result)