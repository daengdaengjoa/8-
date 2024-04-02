from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import DB_app
# from flask_sqlalchemy import SQLAlchemy
# import os
# from flask_paginate import Pagination, get_page_args



app = Flask(__name__)


@app.route("/")
def 메인화면():
    return render_template("메인화면.html")

@app.route("/게시글작성")
def 게시글작성():
    return render_template("게시글 작성.html")

@app.route("/전체글조회", methods=["POST", "GET"])
def 전체글조회():
    # cur = get_cur()  # DB와 연결
    per_page = 10  # 게시글 10개 씩
    # page, _, offset = get_page_args(per_page=per_page)
    print(request.method)

    # POST request라면,
    if request.method == "POST":
        # query = request.form["find"]  # 전체글 조회에서 입력칸에서 받은 "find"글자
        # tag = request.form["tag"]  # 전체글 조회에서 검색방법으로 선택한 "tag"글자
        # query_for_like = ("%" + query + "%").lower()  # 검색 편의를 위해 소문자로 변환
        # 
        # # 게시글 수 파악
        # cur.execute(
        #     "SELECT COUNT(*) FROM 테이블명 "
        #     "WHERE %s LIKE %s;",
        #     (tag, query_for_like),  # 포스트 제목과 내용도 소문자 변환해서 검색
        # )
        # total = cur.fetchone()[0]  #  데이터베이스에서 가져온 결과 집합의 첫 번째 행에서 첫 번째 열의 값
        # 
        # # 게시글 내용
        # cur.execute(
        #     "SELECT p.아이디, 내용, 제목, 날짜, 영화이름, 리뷰, 평점, 이름 "
        #     "FROM 게시글DB p JOIN 유저DB u ON p.아이디 = u.아이디 "
        #     "WHERE %s LIKE %s "
        #     "ORDER BY created DESC;",  # POST라면 LIKE 검색 결과를 보여줌
        #     (tag, query_for_like),
        # )
        total = 1
        posts = [{
            "id": "이름",
            "content": "내용",
            "date": "날짜",
            "title": "제목",
            "movie": "영화이름",
            "review": "리뷰",
            "score": "2",
            "name": "이름",
        }]

    # POST가 아니라면, 즉 GET request라면,
    else:
        # cur.execute("SELECT COUNT(*) FROM 게시글DB p;")  # 게시글 수 파악
        # total = cur.fetchone()[0]
        # 
        # cur.execute(  # GET이라면 검색 없이 모든 포스트를 보여줌
        #     "SELECT p.아이디, 내용, 제목, 날짜, 영화이름, 리뷰, 평점, 이름 "
        #     "FROM 게시글DB p JOIN 유저DB u ON p.아이디 = u.아이디 "
        #     "ORDER BY 날짜 DESC;",  # 생산 일자 역순으로
        #     (per_page, offset),
        # )
        total = 1
        posts = [{
            "id": "billy",
            "content": "content",
            "date": "date",
            "title": "title",
            "movie": "movie",
            "review": "review",
            "score": "score",
            "name": "name",
        },{
            "id": "billy",
            "content": "content",
            "date": "date",
            "title": "title",
            "movie": "movie",
            "review": "review",
            "score": "score",
            "name": "name",
        },]
    print(posts)
    # 모든 데이터 베이스 값 딕셔너리화 하기
    # posts = cur.fetchall()

    return render_template("전체글 조회.html",
                            posts=posts, # 게시글 내용
                            # pagination=Pagination(
                            # page=page,  # 지금 우리가 보여줄 페이지는 1 또는 2, 3, 4, ... 페이지인데,
                            # total=total,  # 총 몇 개의 포스트인지를 미리 알려주고,
                            # per_page=per_page  # 한 페이지당 몇 개의 포스트를 보여줄지 알려주고,
                            # )
    )

@app.route("/게시글조회", methods=["POST", "GET"])
def 게시글조회():

    # # 댓글 로딩
    # cur = get_cur()
    # title = request.form["title"]
    # date = request.form["date"]
    # cur.execute(
    #     "SELECT p.아이디, 댓글내용, 날짜, 이름 "
    #     "FROM 댓글 DB p JOIN 유저DB u ON p.아이디 = u.아이디 "
    #     "WHERE 제목 = %s AND 날짜 = %s"
    #     "ORDER BY 날짜 DESC;",
    #     (title, date),# 생산 일자 역순으로
    # )

    # 모든 데이터 베이스 값 딕셔너리화 하기
    # comment = cur.fetchall()

    comment = {
        "id": "billy",
        "content": "content",
        "date": "date",
        "name": "name"
    }

    return render_template("게시글 조회.html", comment=comment)

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
