from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def 메인화면():
    return render_template("메인화면.html")

@app.route("/게시글작성")
def 게시글작성():
    return render_template("게시글 작성.html")

@app.route("/전체글조회")
def 전체글조회():
    return render_template("전체글 조회.html")

@app.route("/게시글조회")
def 게시글조회():
    return render_template("게시글 조회.html")


if __name__ == "__main__":
    app.run(debug=True)
