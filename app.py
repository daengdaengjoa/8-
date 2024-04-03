from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, request, redirect, url_for, session, flash

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import os
from datetime import datetime


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'  # 이걸 설정을 해야지 로그인 기능을 만들 수 있습니다.. 암호키 같은 기능인가봅니다..
app.config['SQLALCHEMY_DATABASE_URI'] = \
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
    post_id = db.Column(db.String, nullable=False)  # 이거 나중에 추가 되어야 함
    user_id = db.Column(db.String, nullable=False)
    detail = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)


@app.route("/")
def 메인화면():
    print(session.get('user_id'))
    # 로그인 세션정보가 없을 경우
    if not session.get('user_id'):
        posts = Posting.query.order_by(desc(Posting.date)).limit(3).all()
        return render_template("메인화면.html", posts=posts)

    # 로그인 세션정보('user_id')가 있을 경우
    else:
        user_id = session.get('user_id')
        posts = Posting.query.order_by(desc(Posting.date)).limit(3).all()
        return render_template("메인화면.html", posts=posts, user_id=user_id)


@app.route("/로그인화면", methods=["GET", "POST"])
def 로그인화면():
    # 글작성의 내용을 입력하고 작성 완료를 누르면 동작
    # 회원가입 기능!
    if request.method == "POST" and request.form.get("name"):
        # Posting테이블의 칼럼에 맞추어 변수의 값 입력
        new_UserInfo = UserInfo(
            user_id=request.form['user_id'],
            pw=request.form['pw'],
            name=request.form['name'],
            age=request.form['age'],
            gender=request.form['gender'],
            area=request.form['area'],  # 데이터 반영 필요
        )
        # 데이터베이스 세션에 추가
        db.session.add(new_UserInfo)

        # 변경 사항 커밋
        db.session.commit()
        flash("회원 등록 되었습니다.")
        return render_template("로그인 화면.html")
    # 로그인 기능
    elif request.method == "POST" and not request.form.get("name"):
        user_id = request.form.get('user_id')
        pw = request.form.get('pw')
        # 입력받은 값 데이터 베이스에서 조회
        try:
            login = UserInfo.query.filter_by(user_id=user_id, pw=pw).first() # 데이터 베이스에 아디와 비밀번호 맞으면 통과
            if login is not None:
                session["user_id"] = login.user_id
                return redirect(url_for('메인화면'))  # 로그인 성공시 메인화면으로 이동
        # 오류시 로그인 화면 다시 출력
        except:
            flash("입력값이 잘못 되었습니다.")
            return render_template("로그인 화면.html")
    # 데이터 값 저장 만하고 보여줄 필요는 없으니 리턴 값 없음
    return render_template("로그인 화면.html")


@app.route("/로그아웃", methods=["GET"])
def 로그아웃():
    session.clear()  # 세션 값 비워줌으로 로그아웃 처리
    return redirect("/")


@app.route("/게시글작성", methods=["GET", "POST"])
def 게시글작성():
    # 로그인이 되어 있지 않다면 로그인화면으로 이동
    if not session.get('user_id'):
        flash("로그인이 필요한 기능입니다.")
        return render_template("로그인 화면.html")
    # 글작성의 내용을 입력하고 작성 완료를 누르면 동작
    if request.method == "POST":
        # Posting테이블의 칼럼에 맞추어 변수의 값 입력
        new_Posting = Posting(
            user_id=session.get('user_id'),
            username=request.form['username'],
            movie_title=request.form['movie_title'],
            posting_title=request.form['posting_title'],
            review=request.form['review'],
            grade=request.form['rating'],
            date=datetime.now()
        )
        # 데이터베이스 세션에 추가
        db.session.add(new_Posting)

        # 변경 사항 커밋
        db.session.commit()
        flash("게시글이 등록 되었습니다.")
        return redirect("/")

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
        if not session.get('user_id'):
            flash("로그인이 필요한 기능입니다.")
            return render_template("로그인 화면.html")
        new_Comment = Comment(
            post_id=post_id,
            user_id=session.get('user_id'),
            detail=request.form['detail'],
            date=datetime.now()
        )
        # 데이터베이스 세션에 추가
        db.session.add(new_Comment)

        # 변경 사항 커밋
        db.session.commit()
    # 게시글 내용 표시
    comments = Comment.query.filter_by(post_id=post_id).all()

    # query = input('검색할 영화를 입력하세요: ')
    query = posts.movie_title

    url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=' + '%s' % query
    # print(url) # https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=아이언맨3
    response = requests.get(url)
    # print(response) # <Response [200]>
    html_text = response.text
    # print(html_text) # <!doctype html> <html lang="ko"><head> <meta charset="utf-8"> <meta name="referrer" content="always">  <meta name="format-detection" content="telephone=no,address=no,email=no"> <meta property="og:title" content="아이언맨3 : 네이버 통합검색"/> <meta property="og:image" content="https://ssl.pstatic.net/sstatic/search/common/og_v3.png"> <meta property="og:description" content="'아이언맨3'의 네이버 통합검색 결과입니다."> <meta name="description" lang="ko" content="'아이언맨3'의 네이버 통합검색 결과입니다."> <title>아이언맨3 : 네이버 통합검색</title> <link rel="shortcut icon" href="https://ssl.pstatic.net/sstatic/search/favicon/favicon_191118_pc.ico">
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)  #<html lang="ko"><head> <meta charset="utf-8"/> <meta content="always" name="referrer"/> <meta content="telephone=no,address=no,email=no" name="format-detection"/> <meta content="아이언맨3 : 네이버 통합검색" property="og:title"> <meta content="https://ssl.pstatic.net/sstatic/search/common/og_v3.png" property="og:image"/> <meta content="'아이언맨3'의 네이버 통합검색 결과입니다." property="og:description"/> <meta content="'아이언맨3'의 네이버 통합검색 결과입니다." lang="ko" name="description"/> <title>아이언맨3 : 네이버 통합검색</title> <link href="https://ssl.pstatic.net/sstatic/search/favicon/favicon_191118_pc.ico" rel="shortcut icon"/> <link href="https://ssl.pstatic.net/sstatic/search/opensearch-description.https.xml" rel="search" title="Naver" type="application/opensearchdescription+xml"><script> if (top.frames.length!=0 || window!=top) window.open(location, "_top"); </script><link href="https://ssl.pstatic.net/sstatic/search/pc/css/search1_240314.css" rel="stylesheet" type="text/css"/> <link href="https://ssl.pstatic.net/sstatic/search/pc/css/search2_240314

    data1 = {}
    title = soup.select_one('._text').text.strip()
    info = soup.select_one('.info_group dt:contains("개요") + dd').text.strip()
    date = soup.select_one('.info_group dt:contains("개봉") + dd').text.strip()
    star = soup.select_one('.info_group dt:contains("평점") + dd').text.strip()
    nums = soup.select_one('.info_group dt:contains("관객수") + dd').text.strip()
    content = soup.select_one('.desc._text').text.strip()
    image_url = soup.select_one('a.thumb._item img')["src"]

    print(f"{title=} \n {info=} \n {date=} \n {star=} \n {nums=} \n {content=} \n {image_url=}")

    data1 = {'title': title, 'info': info, 'date': date, 'star': star, 'nums': nums, 'content': content,
             'image_url': image_url}

    return render_template("게시글 조회.html", data=data1, comments=comments, posts=posts, login_id=session.get('user_id'))


if __name__ == "__main__":
    app.run(debug=True)

with app.app_context():
    db.create_all()
