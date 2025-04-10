import base64
import requests
from requests.auth import HTTPBasicAuth

def upload_featured_image(site_url, username, app_password, image_url):
    """
    アイキャッチ画像をWordPressにアップロードし、メディアIDを返す
    """
    try:
        image_data = requests.get(image_url).content
        filename = image_url.split("/")[-1]

        headers = {
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Type": "image/jpeg",
        }

        media_url = site_url.rstrip("/") + "/wp-json/wp/v2/media"
        response = requests.post(
            media_url,
            headers=headers,
            data=image_data,
            auth=HTTPBasicAuth(username, app_password)
        )
        response.raise_for_status()
        media_id = response.json().get("id")
        return media_id

    except Exception as e:
        print(f"[画像アップロード失敗] {e}")
        return None


def post_to_wordpress(site_url, username, app_password, title, content, image_url=None):
    """
    記事をWordPressに投稿する（任意でアイキャッチ画像も設定）
    """
    try:
        # アイキャッチ画像のアップロード（任意）
        media_id = None
        if image_url:
            media_id = upload_featured_image(site_url, username, app_password, image_url)

        # 投稿データの構築
        post_data = {
            "title": title,
            "content": content,
            "status": "publish"
        }
        if media_id:
            post_data["featured_media"] = media_id

        post_url = site_url.rstrip("/") + "/wp-json/wp/v2/posts"
        response = requests.post(
            post_url,
            json=post_data,
            auth=HTTPBasicAuth(username, app_password)
        )
        response.raise_for_status()

        print("✅ 投稿成功：", response.json().get("link"))
        return True, response.json().get("link")

    except Exception as e:
        print(f"[投稿失敗] {e}")
        return False, str(e)
