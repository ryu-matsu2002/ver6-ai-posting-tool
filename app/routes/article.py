import os
from flask import Blueprint, render_template, request
from dotenv import load_dotenv
from openai import OpenAI
from app.utils.image_search import search_pixabay_images
import traceback

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

article_bp = Blueprint("article", __name__)

@article_bp.route("/article", methods=["GET", "POST"])
def generate_article():
    article = ""

    if request.method == "POST":
        title = request.form.get("title")

        # 記事生成プロンプト
        content_prompt = f"""
あなたはSEOとコンテンツマーケティングの専門家です。

入力された「Q＆A記事のタイトル」に対しての回答記事を以下の###条件###に沿って書いてください。

###条件###
・文章の構成としては、問題提起、共感、問題解決策の順の構成で書いてください。
・Q＆A記事のタイトルについて悩んでいる人が知りたい事を書いてください。
・見出し（hタグ）を付けてわかりやすく書いてください
・記事の文字数は必ず2500文字〜3500文字程度でまとめてください
・1行の長さは30文字前後にして接続詞などで改行してください。
・「文章の島」は1行から3行以内にして、文章の島同士は2行空けてください
・親友に向けて話すように書いてください（ただし敬語を使ってください）
・読み手のことは「皆さん」ではなく必ず「あなた」と書いてください。

【タイトル】
{title}
"""

        try:
            # GPTで記事本文を生成（max_tokens 少なめにしてタイムアウト回避）
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "あなたは検索意図を深く理解しSEOに強い記事を書ける専門家です"},
                    {"role": "user", "content": content_prompt}
                ],
                temperature=0.7,
                max_tokens=2000,  # ← 減らして応答高速化
            )

            raw_text = response.choices[0].message.content

            # Markdownライク → HTML変換
            html_lines = []
            for block in raw_text.strip().split("\n\n"):
                block = block.strip()
                if block.startswith("###"):
                    content = block.lstrip("#").strip()
                    html_lines.append(f"<h2>{content}</h2>")
                elif block:
                    html_lines.append(f"<p>{block}</p>")

            # Pixabay向け英語キーワード生成
            keyword_prompt = f"""
以下の日本語タイトルに対して、
Pixabayで画像を探すのに最適な英語の2～3語の検索キーワードを生成してください。
抽象的すぎる単語（life, business など）は避けてください。
写真としてヒットしやすい「モノ・場所・情景・体験・風景」などを選んでください。

タイトル: {title}
"""

            keyword_response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "あなたはPixabayで検索されやすい画像キーワードを英語で提案するプロです"},
                    {"role": "user", "content": keyword_prompt}
                ],
                temperature=0.3,
                max_tokens=50,
            )

            image_query = keyword_response.choices[0].message.content.strip()
            image_urls = search_pixabay_images(image_query, max_images=3)

            # 画像を2番目の<h2>以降に挿入
            image_index = 0
            final_html = []

            for i, line in enumerate(html_lines):
                if image_index < len(image_urls) and line.startswith("<h2>") and i != 0:
                    img_tag = f'<img src="{image_urls[image_index]}" style="max-width:100%; margin: 20px 0;">'
                    final_html.append(img_tag)
                    image_index += 1
                final_html.append(line)

            article = "\n".join(final_html)

        except Exception as e:
            # エラー詳細をHTML上に表示（開発時用）
            article = f"<p>エラーが発生しました: {str(e)}</p><pre>{traceback.format_exc()}</pre>"

    return render_template("article.html", article=article)
