from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from bs4 import BeautifulSoup
import requests

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
    # query = input('검색할 영화를 입력하세요: ')
    query = "이터널선샤인"
    url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query='+'%s'%query
    response = requests.get(url)
    html_text = response.text
    soup = BeautifulSoup(response.text, 'html.parser')

    data1 = {}
    title = soup.select_one('._text').text.strip()
    info = soup.select_one('.info_group dt:contains("개요") + dd').text.strip()
    date = soup.select_one('.info_group dt:contains("개봉") + dd').text.strip()
    star = soup.select_one('.info_group dt:contains("평점") + dd').text.strip()
    nums = soup.select_one('.info_group dt:contains("관객수") + dd').text.strip()
    content = soup.select_one('.desc._text').text.strip()
    image_url = soup.select_one('a.thumb._item img')["src"]

    data1 = {'title': title, 'info': info, 'date': date, 'star': star, 'nums': nums, 'content': content, 'image_url': image_url}
    print(data1)
    
    return render_template("게시글 조회.html", data=data1)



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
