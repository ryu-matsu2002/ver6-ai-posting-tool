import os
import re
import requests
from dotenv import load_dotenv

# .env から Pixabay APIキーを読み込み
load_dotenv()
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")


def extract_keywords_from_title(title):
    """
    タイトルから画像検索に使える日本語キーワードを抽出（日本語→英語翻訳を前提とする場合に利用）
    例：「国内旅行で失敗しない旅館の選び方とは？」→「国内 旅行 旅館」
    """
    cleaned = re.sub(r"[^\wぁ-んァ-ン一-龥]", " ", title)
    keywords = [word for word in cleaned.split() if len(word) >= 2]
    return " ".join(keywords[:3])


def search_pixabay_images(query, max_images=3):
    """
    指定した英語クエリでPixabayから画像URLを最大 max_images 件取得する。
    """
    url = "https://pixabay.com/api/"
    params = {
        "key": PIXABAY_API_KEY,
        "q": query,
        "image_type": "photo",
        "orientation": "horizontal",
        "per_page": max_images,
        "safesearch": "true"
        # lang は省略（英語クエリのため）
    }

    try:
        print(f"[Pixabay検索] クエリ: {query}")
        response = requests.get(url, params=params)
        response.raise_for_status()  # HTTPエラーを検知
        data = response.json()

        hits = data.get("hits", [])
        image_urls = [hit["webformatURL"] for hit in hits[:max_images]]

        if not image_urls:
            print("[Pixabay検索] 画像が見つかりませんでした。")

        return image_urls

    except Exception as e:
        print(f"[Pixabay検索エラー] {e}")
        return []
