from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os, datetime

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)

class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    pw = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    area = db.Column(db.String, nullable=False)


class Posting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    movie_title = db.Column(db.String, nullable=False)
    posting_title = db.Column(db.String, nullable=False)
    grade = db.Column(db.Float, nullable=False)
    review = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    detail = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)


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
    user_id_receive = request.form.get("user_id")
    movie_title_receive = request.form.get("movie_title")
    posting_title_receive = request.form.get("posting_title")
    grade_receive = request.form.get("grade")
    review_recieve = request.form.get("review")
    date_receive = datetime.datetime.now()

    posting = Posting(user_id=user_id_receive, movie_title=movie_title_receive,
                      posting_title=posting_title_receive, grade=grade_receive, review=review_recieve,  date=date_receive)
    db.session.add(posting)
    db.session.commit()

    return redirect(url_for('게시글작성'))


@app.route("/login", methods=["POST"])
def login():
    user_id_receive = request.form.get("user_id")
    pw_receive = request.form.get("user_pw")
    name_receive = request.form.get("username")
    age_receive = request.form.get("age")
    gender_receive = request.form.get("gender")
    area_receive = request.form.get("area")
    login = UserInfo(user_id=user_id_receive, user_pw=pw_receive,
                     username=name_receive, age=age_receive, gender=gender_receive, area=area_receive)
    db.session.add(login)
    db.session.commit()
    return redirect(url_for("회원가입"))


@app.route("/comment", methods=["POST"])
def comment():
    user_id_receive = request.form.get("user_id")
    detail_receive = request.form.get("detail")
    date = datetime.now()
    comment = Comment(user_id=user_id_receive,
                      detail=detail_receive, date=date)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for("게시글조회"))

if __name__ == "__main__":
    app.run(debug=True)
