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

@app.route("/submit", methods=["POST"])
def submit():
    author = request.form["author"]
    movie = request.form["movie"]
    title = request.form["title"]
    content = request.form["content"]
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 여기서 데이터베이스에 데이터를 저장
    print("작성 시간:", current_time)
    print("작성자:", author)
    print("영화 이름:", movie)
    print("제목:", title)
    print("내용:", content)
    return redirect(url_for("게시글작성"))


if __name__ == "__main__":
    app.run(debug=True)
