from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, request, redirect, url_for, session, flash

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import os
from datetime import datetime

from openai import OpenAI

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SECRET_KEY"] = (
    "1234"  # 이걸 설정을 해야지 로그인 기능을 만들 수 있습니다.. 암호키 같은 기능인가봅니다..
)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "database.db"
)

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
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)


class Comment(db.Model):  # 댓글 정보 데이터
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.String, nullable=False)
    user_id = db.Column(db.String, nullable=False)
    detail = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)


class Crawling(db.Model):  # 크롤링 정보 데이터
    id = db.Column(db.Integer, primary_key=True)
    title_user = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    info = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    star = db.Column(db.String, nullable=False)
    nums = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=False)
    title_user = db.Column(db.String, nullable=False)


# 서버가 열리면 로그인되어 있던 모든 기록이 초기화 시킬 수 있도록 하는 기능
@app.before_request
def clear_session():
    if not app.config.get('_got_first_request', None):
        session.clear()  # 서버가 시작될 때 세션을 초기화합니다.
        app.config['_got_first_request'] = True


@app.route("/")
def 메인화면():
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
            user_id=request.form["user_id"],
            pw=request.form["pw"],
            name=request.form["name"],
            age=request.form["age"],
            gender=request.form["gender"],
            area=request.form["area"],  # 데이터 반영 필요
        )
        # 데이터베이스 세션에 추가
        db.session.add(new_UserInfo)

        # 변경 사항 커밋
        db.session.commit()
        flash("회원 등록 되었습니다.")
        return render_template("로그인 화면.html")
    # 로그인 기능
    elif request.method == "POST" and not request.form.get("name"):
        user_id = request.form.get("user_id")
        pw = request.form.get("pw")
        # 입력받은 값 데이터 베이스에서 조회
        try:
            login = UserInfo.query.filter_by(
                user_id=user_id, pw=pw
            ).first()  # 데이터 베이스에 아디와 비밀번호 맞으면 통과
            if login is not None:
                session["user_id"] = login.user_id
                return redirect(url_for("메인화면"))  # 로그인 성공시 메인화면으로 이동
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
    if not session.get("user_id"):
        flash("로그인이 필요한 기능입니다.")
        return render_template("로그인 화면.html")
    # 글작성의 내용을 입력하고 작성 완료를 누르면 동작
    if request.method == "POST":
        # Posting테이블의 칼럼에 맞추어 변수의 값 입력
        new_Posting = Posting(
            user_id=session.get("user_id"),
            username=request.form["username"],
            movie_title=request.form["movie_title"],
            posting_title=request.form["posting_title"],
            review=request.form["review"],
            grade=request.form["rating"],
            date=datetime.now(),
            views=0,
            likes=0,
        )

        query = request.form["movie_title"] + "영화"
        print(query)
        url = (
                "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query="
                + "%s" % query
        )
        response = requests.get(url)
        html_text = response.text
        soup = BeautifulSoup(response.text, "html.parser")

        data1 = {}
        try:
            title = soup.select_one("._text").text.strip()
        except AttributeError:
            title = "-"
        try:
            info = soup.select_one('.info_group dt:contains("개요") + dd').text.strip()
        except AttributeError:
            info = "-"
        try:
            date = soup.select_one('.info_group dt:contains("개봉") + dd').text.strip()
        except AttributeError:
            date = "-"
        try:
            star = soup.select_one('.info_group dt:contains("평점") + dd').text.strip()
        except AttributeError:
            star = "-"
        try:
            nums = soup.select_one('.info_group dt:contains("관객수") + dd').text.strip()
        except AttributeError:
            nums = "-"
        try:
            content = soup.select_one(".desc._text").text.strip()
        except AttributeError:
            content = "-"
        image_element = soup.select_one("a.thumb._item img")
        if image_element:
            image_url = image_element["src"]
        else:
            image_url = "https://lh6.googleusercontent.com/proxy/fDnxsdswqStDDt7hMOlRk6C7OMjZD1dJ2SYJjdQ-UEb83LfqzWqljAIS4F0oN9Q9L1vl4bK87cmATi5ueHvTbA"

        existing_entry = Crawling.query.filter_by(title=title).first()
        if existing_entry:
            print("이미존제하는영화")
        else:
            new_Crawling = Crawling(
                title=title,
                info=info,
                date=date,
                star=star,
                nums=nums,
                content=content,
                image_url=image_url,
                title_user=request.form["movie_title"]
            )
            db.session.add(new_Crawling)

        db.session.add(new_Posting)

        # 변경 사항 커밋
        db.session.commit()
        flash("게시글이 등록 되었습니다.")
        return redirect("/")

    # 데이터 값 저장 만하고 보여줄 필요는 없으니 리턴 값 없음
    return render_template("게시글 작성.html")


@app.route("/AI추천", methods=["GET", "POST"])
def AI추천():
    data_ai = "질문해주세요"
    m1 = ""
    m2 = ""
    m1_plus = ""
    # 글작성의 내용을 입력하고 작성 완료를 누르면 동작
    if request.method == "POST":

        client = OpenAI(api_key="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")

        query = request.form["ask"]

        response0 = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {
                    "role": "system",
                    "content": "역할: 영화 평론가, 작업: 제목과 1점에서 10점사이의 추천도와 추천이유를 제공하여 사용자에게 영화를 추천하고,"
                               + "선택 항목은 지난 30년간의 영화이며 TV 시리즈가 포함되지 않도록 합니다. 또한 추천도는 엄격한기준으로 매깁니다."
                               + "또한 같은영화를 추천하지 않으며 영화제목은 한글과 영문 모두 출력합니다.",
                },
                {"role": "user", "content": query},
            ],
        )

        messages = [{"role": "user", "content": response0.choices[0].message.content}]

        function1 = [
            {
                "name": "get_movie_title",
                "description": "영화의영문 제목을 찾아서 알려줍니다.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "movie_title": {
                            "type": "string",
                            "description": "영화이름 eg. 레옹, 대부, 인터스텔라",
                        },
                    },
                    "required": ["movie_title"],
                },
            }
        ]
        function2 = [
            {
                "name": "get_movie_star",
                "description": "영화의 점수를 찾아서 알려줍니다.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "movie_star": {
                            "type": "string",
                            "description": "영화점수 eg. 10/10, 9/10, 5/10, 6점",
                        },
                    },
                    "required": ["movie_star"],
                },
            }
        ]

        response1 = client.chat.completions.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            functions=function1,
            function_call="auto",
        )

        response2 = client.chat.completions.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            functions=function2,
            function_call="auto",
        )

        response_message1 = response1.choices[0].message
        response_message2 = response2.choices[0].message
        data_ai = response0.choices[0].message.content

        m1_0 = str(response_message1)
        m2_0 = str(response_message2)

        print(response0.choices[0].message.content)
        print(response_message1)
        print(response_message2)
        try:
            m1 = m1_0.split(":")[1].split('"')[1].strip()
        except AttributeError:
            m1 = ""
        try:
            m2 = m2_0.split(":")[1].split('"')[1].strip()
        except AttributeError:
            m2 = ""

        m1_plus = m1 + "영화"

    query = m1_plus
    url = (
            "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query="
            + "%s" % query
    )
    response = requests.get(url)
    html_text = response.text
    soup = BeautifulSoup(response.text, "html.parser")

    data1 = {}
    try:
        title = soup.select_one("._text").text.strip()
    except AttributeError:
        title = "-"
    try:
        info = soup.select_one('.info_group dt:contains("개요") + dd').text.strip()
    except AttributeError:
        info = "-"
    try:
        date = soup.select_one('.info_group dt:contains("개봉") + dd').text.strip()
    except AttributeError:
        date = "-"
    try:
        star = soup.select_one('.info_group dt:contains("평점") + dd').text.strip()
    except AttributeError:
        star = "-"
    try:
        nums = soup.select_one('.info_group dt:contains("관객수") + dd').text.strip()
    except AttributeError:
        nums = "-"
    try:
        content = soup.select_one(".desc._text").text.strip()
    except AttributeError:
        content = "-"
    image_element = soup.select_one("a.thumb._item img")
    if image_element:
        image_url = image_element["src"]
    else:
        image_url = "https://lh6.googleusercontent.com/proxy/fDnxsdswqStDDt7hMOlRk6C7OMjZD1dJ2SYJjdQ-UEb83LfqzWqljAIS4F0oN9Q9L1vl4bK87cmATi5ueHvTbA"

    data1 = {
        "title": title,
        "info": info,
        "date": date,
        "star": star,
        "nums": nums,
        "content": content,
        "image_url": image_url,
    }

    return render_template("AI추천.html", data_ai=data_ai, m1=m1, m2=m2, data1=data1)


@app.route("/전체글조회", methods=["POST", "GET"])
def 전체글조회():
    # POST 입력을 받고 왔으면 조건문 입장
    if request.method == "POST":
        # post로 가져온 매개변수를 각각 넣어준다.
        find = request.form.get("find")
        tag = request.form.get("tag")
        # Posting 테이블에서 tag=검색 조건에 해당하는 칼럼에서 find의 내용을 포함하는 값이 있다면 모두 가져온다.
        posts = (
            Posting.query.filter(getattr(Posting, tag).like(f"%{find}%"))
            .order_by(desc(Posting.date))
            .all()
        )

        POSTS_PER_PAGE = 30
        # 페이지 번호 가져오기
        page = request.args.get("page", 1, type=int)
        # 해당 페이지에 표시할 게시글 범위 계산
        start_index = (page - 1) * POSTS_PER_PAGE
        end_index = start_index + POSTS_PER_PAGE
        # 현재 페이지에 해당하는 게시글만 추출
        displayed_posts = posts[start_index:end_index]
        # 전체 페이지 수 계산
        total_pages = len(posts) // POSTS_PER_PAGE + (len(posts) % POSTS_PER_PAGE > 0)
        return render_template(
            "전체글 조회.html",
            posts=displayed_posts,
            total_pages=total_pages,
            current_page=page,
        )

    # 검색기능을 하지 않고 처음들어올 때에는 모든 게시글이 보일 수 있도록 한다.
    else:
        posts = Posting.query.order_by(desc(Posting.date)).all()

        POSTS_PER_PAGE = 5
        # 페이지 번호 가져오기
        page = request.args.get("page", 1, type=int)
        # 해당 페이지에 표시할 게시글 범위 계산
        start_index = (page - 1) * POSTS_PER_PAGE
        end_index = start_index + POSTS_PER_PAGE
        # 현재 페이지에 해당하는 게시글만 추출
        displayed_posts = posts[start_index:end_index]
        # 전체 페이지 수 계산
        total_pages = len(posts) // POSTS_PER_PAGE + (len(posts) % POSTS_PER_PAGE > 0)
        return render_template(
            "전체글 조회.html",
            posts=displayed_posts,
            total_pages=total_pages,
            current_page=page,
        )


@app.route("/게시글조회", methods=["POST", "GET"])
def 게시글조회():
    # 전체글에서 게시글을 클릭해서 들어올 때에 해당하는 게시글에 맞추어서 글과 댓글을 가져올 수 있도록
    post_id = request.args.get("post_id")
    # 게시글 아이디에 맞추어 글의 내용을 가져온다.
    posts = Posting.query.filter_by(id=post_id).first()

    # 게시글을 이전에 방문했는지 확인하기 위해 세션 사용
    visited_posts = session.get('visited_posts', [])
    if post_id not in visited_posts:
        # 이전에 방문하지 않은 게시글일 경우 조회수 증가
        posts.views += 1
        visited_posts.append(post_id)
        session['visited_posts'] = visited_posts

        # 조회수를 데이터베이스에 반영
        db.session.commit()

    print(posts.views)
    # POST시 댓글 저장한다.
    if request.method == "POST":
        if not session.get("user_id"):
            flash("로그인이 필요한 기능입니다.")
            return render_template("로그인 화면.html")
        if request.form.get("detail"):
            new_Comment = Comment(
                post_id=post_id,
                user_id=session.get("user_id"),
                detail=request.form["detail"],
                date=datetime.now(),
            )
            # 데이터베이스 세션에 추가
            db.session.add(new_Comment)

            # 변경 사항 커밋
            db.session.commit()

        elif request.form.get("like"):
            # 게시글을 이전에 좋아요했는지 확인하기 위해 세션 사용
            liked_posts = session.get('liked_posts', [])
            if post_id in liked_posts:
                # 이미 좋아요를 누른 게시글일 경우
                # 좋아요를 취소하고 세션에서 해당 게시글을 제거
                liked_posts.remove(post_id)
                session['liked_posts'] = liked_posts
                # 좋아요 횟수를 데이터베이스에서 차감
                posts.likes -= 1

            else:
                # 이전에 좋아요를 누르지 않은 게시글일 경우
                # 좋아요를 처리하고 좋아요한 게시글을 세션에 추가
                liked_posts.append(post_id)
                session['liked_posts'] = liked_posts
                # 좋아요 횟수를 데이터베이스에 반영
                posts.likes += 1

            # 데이터베이스 변경 사항 커밋
            db.session.commit()

    # 게시글 내용 표시
    comments = Comment.query.filter_by(post_id=post_id).all()

    title = posts.movie_title

    data1 = Crawling.query.filter_by(title_user=title).first()

    print(data1)
    return render_template(
        "게시글 조회.html", data=data1, comments=comments, posts=posts, login_id=session.get('user_id'), button=post_id in session.get('liked_posts', []))


if __name__ == "__main__":
    app.run(debug=True)

with app.app_context():
    db.create_all()
