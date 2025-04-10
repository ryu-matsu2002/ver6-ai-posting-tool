import os
from flask import Blueprint, render_template, request
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

title_bp = Blueprint("title", __name__)

@title_bp.route("/title", methods=["GET", "POST"])
def generate_title():
    titles = []

    if request.method == "POST":
        keyword = request.form.get("keyword")

        prompt = f"""
あなたはSEOとコンテンツマーケティングの専門家です。

入力されたキーワードを使って
WEBサイトのQ＆A記事コンテンツに使用する「記事タイトル」を10個考えてください。

記事タイトルには必ず入力されたキーワードを全て使ってください  
キーワードの順番は入れ替えないでください  
最後は「？」で締めてください

【キーワード】
{keyword}

###具体例###

「転職 時期」というキーワードに対する出力文：  
転職に有利な時期があるって本当ですか？

「転職 面接 聞かれること」というキーワードに対する出力文：  
転職面接で必ず聞かれることとは？
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "あなたはSEOとコンテンツマーケティングの専門家です。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                top_p=1.0,
                max_tokens=800
            )

            titles_text = response.choices[0].message.content
            titles = [line.strip() for line in titles_text.strip().split("\n") if line.strip()]

        except Exception as e:
            titles = [f"エラーが発生しました: {str(e)}"]

    return render_template("title.html", titles=titles)
