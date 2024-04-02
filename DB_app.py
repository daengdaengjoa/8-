from flask import Flask, request, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')

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
    review = db.Column(db.String, nullable=False)
    grade = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    detail = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)


@app.route("/submit", methods=["POST"])
def submit():
    user_id_receive = request.form.get("author")
    movie_title_receive = request.form.get("movie_title")
    posting_title_receive = request.form.get("posting_title")
    review_recieve = request.form.get("review")
    grade_receive = request.form.get("grade")
    date_receive = request.form.get("date")

    posting = Posting(author=user_id_receive, movie_title=movie_title_receive,
                      posting_title=posting_title_receive, review=review_recieve, grade=grade_receive, date=date_receive)
    db.session.add(posting)
    db.session.commit()

    #     # 여기서 데이터베이스에 데이터를 저장
    # print("작성 시간:", current_time)
    # print("작성자:", author)
    # print("영화 이름:", movie)
    # print("제목:", title)
    # print("내용:", content)
    # return redirect(url_for("게시글작성"))
    return redirect(url_for('게시글 작성'))


with app.app_context():
    db.create_all()
