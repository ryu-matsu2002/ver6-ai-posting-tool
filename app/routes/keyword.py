import os
from flask import Blueprint, render_template, request
from dotenv import load_dotenv
from openai import OpenAI

# .envからAPIキーを読み込み
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# BlueprintにURLプレフィックスを追加
keyword_bp = Blueprint("keyword", __name__, url_prefix="/keyword")

@keyword_bp.route("/", methods=["GET", "POST"])
def index():
    keywords = []

    if request.method == "POST":
        genre = request.form.get("genre")

        # SEOに強いロングテールキーワードを生成するためのプロンプト
        prompt = f"""
ジャンル: {genre}

あなたはGoogle検索に詳しいSEOキーワードの専門家です。
Google Suggest、Googleトレンド、Ubersuggest、キーワードプランナーの知見をもとに、
検索ボリュームがありSEOに強い「3語以上の日本語のロングテールキーワード」を10個生成してください。

【条件】
- 単語数は必ず3語以上にする
- 単語の区切りは半角スペース（例：転職 未経験 IT）
- 出力は番号なし、リスト形式（1行に1キーワード）
- 実際に検索されているような自然なキーワードにしてください
"""

        try:
            # ChatGPT API（gpt-4-turbo）を使って生成
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "あなたはGoogle検索キーワードを設計するSEOのプロです。検索意図を理解し、自然検索で使用されるフレーズを生成してください。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                top_p=1.0,
                max_tokens=800,
            )

            keywords_text = response.choices[0].message.content
            keywords = [line.strip() for line in keywords_text.strip().split("\n") if line.strip()]

        except Exception as e:
            keywords = [f"エラーが発生しました: {str(e)}"]

    return render_template("index.html", keywords=keywords)
