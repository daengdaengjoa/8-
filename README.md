# 🗣️Project: CineChat
#### 영화 리뷰와 댓글로 소통하고, AI가 취향맞춤 영화 추천을 해주는 웹사이트

<br>

## 👨‍🏫 Project Introduction
<p>프로젝트의 시작점은 영화를 좋아하는 Team-8의 구성원들이 서로의 취향과 의견을 공유할 수 있는 웹사이트를 만들어 보기로 한 것입니다.</p>
<p>하지만 저희의 궁극적인 목표는 CineChat을 통해 Team-8 구성원 뿐만 아니라 영화를 사랑하는 모든 분들이 다양한 의견을 나눌 수 있게 하는 것이었습니다.</p>
<p>이를 위해 CineChat은 영화 리뷰 작성과 그에 대한 댓글 작성, 그리고 Chat GPT를 통한 영화추천 기능을 제공합니다.</p>

<br>

## ⏲️ Development time
- 2024.04.01(월) ~ 2023.04.05(금)
- 아이디어 노트 작성
- 아이디어 발표
- 와이어프레임 및 SA문서 작성
- 기능구현
- 발표
<br>

## 🧑‍🤝‍🧑 Development Team: Team-8 
- **김도연** : 
- **김준수** : 
- **박현준** : 게시글 검색 기능, 로그인/로그아웃, 회원가입 및 로그인 상태에서 게시물 작성 가능여부, 관리자 계정 생성후 관리기능, merge 후 오류수정, 좋아요/조회수 기능
- **박소영** : Database table 제작, 게시물 수정 및 삭제, 댓글 수정 및 삭제
- **박해원** : 

- 예시
이윤재 - 영화 예매, 영화 업로드, Database Script 제작, 통합 및 형상관리
채현우 - 로그인, 회원가입, ID찾기, PW찾기, 마이 페이지,메인 페이지, 통합 및 형상관리, PPT제작, 발표
이종원 - 메인 페이지, 메인 CSS
전성덕 - 1대1 문의 게시판(CRUD), 공지사항 게시판(CRUD)
김창훈 - 1대1 문의 게시판(CRUD), 공지사항 게시판(CRUD)
김성재 - 로그인, 회원가입, ID찾기, PW찾기
  
![개발자 소개](이미지 링크 추후에 git헙에 추가)

<br>

## 💻 Development Environment
- **Programming Language** : Python 3.x
- **Web Framework** : Flask
- **Template Engine** : Jinja2
- **Database** : SQLite (for development and testing), PostgreSQL (for deployment)
- **IDE** : Visual Studio Code, PyCharm
- **Version Control** : Git, GitHub
<br>

## ⚙️ Technology Stack
- **Frontend** : HTML, CSS, JavaScript
- **Backend** : Flask
- **Database ORMR** : SQLAlchemy
- **Idea Brainstorming Tools and Environments** : Slack, Zep, Notion, figma
<br>

## 📝 Project Architecture
![프로젝트 아키텍쳐]()

<br>

## 📌 Key Features

### 1. Post CRUD
   - Users can create new posts and view all posts.
   - Posts can be edited or deleted on the post detail view page.

### 2. Comment CRUD
   - All comments on the post are displayed at the bottom of the post detail view page.
   - Users can create, view, edit, and delete comments on the post detail page.

### 3. AI Movie Recommendation
   - Users can directly ask the AI for movie recommendations based on specified conditions.
   - Movie recommendations generated by the AI are displayed within the page
     
### 4.  Sign Up, Log In
   - Membership registration is mandatory for first-time users, enabling them to log in and access the site's features.
   - Only logged-in users can create posts, while both logged-in and anonymous users can view posts and comments.
     
### 5.  Search Functionality
   - Users can search for posts by movie name, article title, author, and content using the post search box.
   - Clicking on search results directs users to the detailed page of the respective post.

### 6. Movie Information Crawling
   - In addition to user-generated movie reviews, crawled movie information from an external API is displayed on the post detail page.
   - Movie details obtained from the Crawling include images, overview, release date, rating, number of viewers, plot, etc.
     
### 7. Like Feature
   - Users can like posts on the post details view page.
   - The 'Like' button toggles to 'Dislike' upon clicking and can be undone, allowing users to like a post only once.
     
### 8. Administrator Permissions
   - Administrators with the ID "admin_team8" have the authority to edit or delete posts and comments, irrespective of the post's author.
     

<br> 

## ✒️ API
###  API-1
엔드포인트	메서드	요청 바디	응답
   - signup	POST	user_id, pw, name, age, gender, area	200 OK, 400 Bad Request, 409 Conflict  
   - login	POST	user_id, pw	200 OK, 400 Bad Request, 401 Unauthorized
   - logout	GET	-	200 OK
   - write_post	POST	user_id, movie_title, posting_title, review, rating	200 OK, 400 Bad Request, 401 Unauthorized
   - get_post/<post_id>	GET	-	200 OK, 404 Not Found
   - update_post/<post_id>	POST	movie_title, posting_title, review, rating	200 OK, 400 Bad Request, 401 Unauthorized, 404 Not Found
   - delete_post/<post_id>	GET	-	200 OK, 401 Unauthorized, 404 Not Found
   - write_comment/<post_id>	POST	detail	200 OK, 400 Bad Request, 401 Unauthorized, 404 Not Found
-/get_comments/<post_id>	GET	-	200 OK, 404 Not Found
-/update_comment/<comment_id>	POST	detail	200 OK, 400 Bad Request, 401 Unauthorized, 404 Not Found
-/delete_comment/<comment_id>	GET	-	200 OK, 401 Unauthorized, 404 Not Found

