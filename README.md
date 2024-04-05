# 🗣️Project: CineChat
#### 영화 리뷰와 댓글로 소통하고, AI가 취향맞춤 영화 추천을 해주는 웹사이트

<br>

## 👨‍🏫 Project Introduction
CineChat은 영화 리뷰 작성과 그에 대한 댓글 작성, 그리고 Chat GPT를 통한 영화추천 기능을 제공합니다.

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
- **김준수** : AI영화 추천 기능, 영화정보(포스터,평점,개봉일등)크롤링 및 DB업로드/출력, 전체글 페이지네이션, 초기 HTML 구조 제작  
- **박현준** : 게시글 검색 기능, 로그인/로그아웃, 회원가입 및 로그인 상태에서 게시물 작성 가능여부, 관리자 계정 생성후 관리기능, merge 후 오류수정, 좋아요/조회수 기능
- **박소영** : Database table 제작, 게시물 수정 및 삭제, 댓글 수정 및 삭제
- **박해원** : DB table, CSS/접근성(accessibility) 향상


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
S.A. 노션 : https://www.notion.so/teamsparta/S-A-8-a04adb1fb1884d80aa92feea44fb70d0
![image](https://github.com/daengdaengjoa/Team-8/assets/157565164/a8ab58ef-e818-44f3-a27e-32b8c3ed7c40)


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
| 엔드포인트               | 메서드 | 요청 본문 데이터             | 응답 코드                             |
|------------------------|--------|------------------------------|--------------------------------------|
| /signup                | POST   | user_id, pw, name, age, gender, area | 200 OK, 400 Bad Request, 409 Conflict |
| /login                 | POST   | user_id, pw                  | 200 OK, 400 Bad Request, 401 Unauthorized |
| /logout                | GET    | -                            | 200 OK                               |
| /write_post            | POST   | user_id, movie_title, posting_title, review, rating | 200 OK, 400 Bad Request, 401 Unauthorized |
| /get_post/<post_id>   | GET    | -                            | 200 OK, 404 Not Found                |
| /update_post/<post_id>| POST   | movie_title, posting_title, review, rating | 200 OK, 400 Bad Request, 401 Unauthorized, 404 Not Found |
| /delete_post/<post_id>| GET    | -                            | 200 OK, 401 Unauthorized, 404 Not Found |
| /write_comment/<post_id> | POST | detail                       | 200 OK, 400 Bad Request, 401 Unauthorized, 404 Not Found |
| /get_comments/<post_id>| GET    | -                            | 200 OK, 404 Not Found                |
| /update_comment/<comment_id> | POST | detail                   | 200 OK, 400 Bad Request, 401 Unauthorized, 404 Not Found |
| /delete_comment/<comment_id>| GET | -                          | 200 OK, 401 Unauthorized, 404 Not Found |


- API 명세서 : <>
