import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)


class UserInfo(db.Model):  # 유저 정보 데이터
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    pw = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    area = db.Column(db.String, nullable=False)


class Posting(db.Model):  # 게시글 정보 데이터
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    movie_title = db.Column(db.String, nullable=False)
    posting_title = db.Column(db.String, nullable=False)
    review = db.Column(db.String, nullable=False)
    grade = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)


class Comment(db.Model):  # 댓글 정보 데이터
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.String, nullable=False) # 이거 나중에 추가 되어야 함
    user_id = db.Column(db.String, nullable=False)
    detail = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)


@app.route("/")
def 메인화면():
    posts = Posting.query.order_by(desc(Posting.date)).limit(3).all()
    return render_template("메인화면.html", posts=posts)


@app.route("/게시글작성", methods=["GET", "POST"])
def 게시글작성():
    # 글작성의 내용을 입력하고 작성 완료를 누르면 동작
    if request.method == "POST":
        # Posting테이블의 칼럼에 맞추어 변수의 값 입력
        new_Posting = Posting(
            user_id='123', # 아직 유저 정보 없음....
            username=request.form['username'],
            movie_title=request.form['movie_title'],
            posting_title=request.form['posting_title'],
            review=request.form['review'],
            grade='3',  # 데이터 반영 필요
            date=datetime.now()
        )
        # 데이터베이스 세션에 추가
        db.session.add(new_Posting)

        # 변경 사항 커밋
        db.session.commit()
    # 데이터 값 저장 만하고 보여줄 필요는 없으니 리턴 값 없음
    return render_template("게시글 작성.html")


@app.route("/전체글조회", methods=["POST", "GET"])
def 전체글조회():
    # POST 입력을 받고 왔으면 조건문 입장
    if request.method == "POST":
        # post로 가져온 매개변수를 각각 넣어준다.
        find = request.form.get("find")
        tag = request.form.get("tag")
        # Posting 테이블에서 tag=검색 조건에 해당하는 칼럼에서 find의 내용을 포함하는 값이 있다면 모두 가져온다.
        posts = Posting.query.filter(getattr(Posting, tag).like(f"%{find}%")).all()

    # 검색기능을 하지 않고 처음들어올 때에는 모든 게시글이 보일 수 있도록 한다.
    else:
        posts = Posting.query.all()

    return render_template("전체글 조회.html", posts=posts)  # 게시글 내용


@app.route("/게시글조회", methods=["POST", "GET"])
def 게시글조회():
    # 전체글에서 게시글을 클릭해서 들어올 때에 해당하는 게시글에 맞추어서 글과 댓글을 가져올 수 있도록
    post_id = request.args.get("post_id")
    # 게시글 아이디에 맞추어 글의 내용을 가져온다.
    posts = Posting.query.filter_by(id=post_id).first()

    # POST시 댓글 저장한다.
    if request.method == "POST":
        new_Comment = Comment(
            post_id=post_id,
            user_id="심청이",
            detail=request.form['detail'],
            date=datetime.now()
        )
        # 데이터베이스 세션에 추가
        db.session.add(new_Comment)

        # 변경 사항 커밋
        db.session.commit()
    # 게시글 내용 표시
    comments = Comment.query.filter_by(post_id=post_id).all()

    return render_template("게시글 조회.html", comments=comments, posts=posts)


@app.route("/submit", methods=["POST"])
def submit():
    author = request.form["author"]
    movie = request.form["movie"]
    title = request.form["title"]
    content = request.form["content"]
    current_time = datetime.now()

    # 여기서 데이터베이스에 데이터를 저장
    print("작성 시간:", current_time)
    print("작성자:", author)
    print("영화 이름:", movie)
    print("제목:", title)
    print("내용:", content)
    return redirect(url_for("게시글작성"))


if __name__ == "__main__":
    app.run(debug=True)

with app.app_context():
    db.create_all()
