# pip로 다운 
- 한번에 다운
```
pip install Flask Flask-SQLAlchemy Werkzeug Flask-Login python-dotenv google-generativeai Authlib
```

- Flask 설치
```
pip install flask
```

- 설치 확인
```
python -m flask --version
```
-  SQLAlchemy(데이터베이스 ORM)
```
pip install Flask-SQLAlchemy
```
- Flask의 내부에서 사용되는 WSGI 유틸리티 라이브러리 (할 필요 없음)
```
pip install Werkzeug
```
- 사용자 세션 관리를 위한 확장
```
pip install Flask-Login
```
- .env 파일에 환경 변수(예: SECRET_KEY, GOOGLE_CLIENT_ID, GENAI_API_KEY)를 저장하고 로드하는 데 사용
```
pip install python-dotenv
```
- Google Gemini API와 상호작용하기 위한 
```
pip install google-generativeai
```
- Google OAuth 2.0 연동을 위해 사용되는 라이브러리
```
pip install Authlib
```

# pip 다운이 안 된다면 
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```
```
python get-pip.py
```
# 파일 전체 흐름
```
myweb/
├── app.py                  # Flask 애플리케이션의 핵심 로직 (백엔드)
├── .env                    # 환경 변수 (API 키, 시크릿 키 등)
├── templates/              # HTML 템플릿 파일 (프론트엔드)
│   ├── index.html          # 메인 페이지
│   ├── bulletin_board.html # 일반 게시판 목록
│   ├── edit_post.html      # 문의 게시글 수정 폼
│   ├── login.html          # 로그인 페이지
│   ├── new_bulletin_post.html # 일반 게시글 작성 폼
│   ├── new_post.html       # 문의 게시글 작성 폼
│   ├── register.html       # 회원가입 페이지
│   ├── view.html           # 문의 게시글 상세 보기
│   ├── view_bulletin_post.html # 일반 게시글 상세 보기
│   ├── building/           # 건물 정보 페이지
│   │   ├── B01.html
│   │   ├── B26.html
│   │   └── B27.html
│   └── board.html          # 문의 게시판 목록
├── static/                 # 정적 파일 (CSS, JavaScript, 이미지)
│   ├── buildingC/          # 건물별 CSS
│   │   └── B01.css
│   ├── images/             # 이미지 파일
│   │   └── ...
│   ├── board.css           # 문의 게시판 스타일
│   ├── bulletin_board.css  # 일반 게시판 스타일
│   ├── comments.css        # 댓글 스타일
│   ├── image_slider.css    # 이미지 슬라이더 스타일
│   ├── image_slider.js     # 이미지 슬라이더 JavaScript
│   ├── style.css           # 전역 스타일
│   └── view.css            # 게시글 상세 보기 스타일
└── instance/               # 데이터베이스 파일
    └── database.db         # SQLite 데이터베이스 파일
```
- `app.py`는 모든 백엔드 로직을 처리하며, `templates` 폴더의 HTML 파일들을 렌더링하여 사용자에게 보여줍니다.
- `static` 폴더는 웹 페이지의 디자인과 동적인 요소를 담당하는 CSS, JavaScript, 이미지 파일들을 포함합니다.
- `instance` 폴더에는 SQLite 데이터베이스 파일이 저장됩니다.
- `.env` 파일은 민감한 API 키와 같은 환경 변수를 안전하게 관리하는 데 사용됩니다.

# 웹 페이지 구성하기

## index.html 
```
<!DOCTYPE html>
<html lang="ko">

<head>
    <meta charset="UTF-8">
    <title>회원 관리 및 일반 게시판</title> 
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>

<body>
    <header class="main-header">
        <div class="logo">경성대학교 꿀팁!</div>
    </header>

</body>

</html>
```
 
## app.py 
```
from flask import Flask, render_template # render_template을 import 합니다.

# 1. Flask 애플리케이션 인스턴스 생성
app = Flask(__name__, template_folder='templates')

# 2. 기본 경로('/')에 대한 라우트 정의
@app.route('/')
def home():
    return render_template('index.html') # templates 폴더의 index.html을 렌더링합니다.

# 애플리케이션 실행
if __name__ == '__main__':
    app.run(debug=True)  # 디버깅 모드에서 애플리케이션 실행
    #app.run(host='0.0.0.0', port=8000, debug=True)  # 호스트와 포트를 지정하여 실행할 경우
```

## style.css 
```
/* 기본 스타일 초기화 */
body,
h1,
h2,
h3,
p,
ul,
li {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f0f4f8; /* 밝은 회색 배경 */
    color: #003060;
    line-height: 1.6;
}

/* 헤더 스타일 */
.main-header {
    background-color: #004080; /* 메인 파란색 */
    color: white;
    padding: 10px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 1.5em;
    font-weight: bold;
}
```

# 데이터베이스 구축  
## app.py 수정 - 코드를 작성하면 자동으로 데이터베이스 구축 
```
from flask import Flask, render_template # render_template을 import 합니다.
from flask_sqlalchemy import SQLAlchemy

# 1. Flask 애플리케이션 인스턴스 생성
app = Flask(__name__, template_folder='templates') 

# 2. SQLALCHEMY_DATABASE_URI 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # SQLite 데이터베이스 사용
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 비활성화하여 메모리 오버헤드 줄이기 

# 3. SQLAlchemy 인스턴스 초기화
db = SQLAlchemy(app)

# 4. 데이터베이스 모델 정의 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# 5. 애플리케이션 컨텍스트 내에서 데이터베이스 테이블 생성
with app.app_context():
    db.create_all()

# 6. 기본 경로('/')에 대한 라우트 정의 (이전 코드에서 추가)
@app.route('/')
def home():
    # 여기서 데이터베이스에서 사용자 정보를 가져와 index.html에 전달할 수 있습니다.
    users = User.query.all() # 모든 User 객체를 가져옴
    return render_template('index.html', users=users) # templates 폴더의 index.html을 렌더링합니다.

# 7. 애플리케이션 실행
if __name__ == '__main__':
    app.run(debug=True)  # 디버깅 모드에서 애플리케이션 실행
    #app.run(host='0.0.0.0', port=8000, debug=True)  # 호스트와 포트를 지정하여 실행할 경우

```

# 회원 관리 (로그인 페이지)
## login.html (추가) 
```
<!DOCTYPE html>
<html>
<head>
    <title>로그인</title>
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <h1>로그인</h1>
    <form method="POST">
        <label for="username">사용자 이름:</label><br>
        <input type="text" id="username" name="username" required><br><br>
        <label for="password">비밀번호:</label><br>
        <input type="password" id="password" name="password" required><br><br>
        <input type="submit" value="로그인">
    </form>
    <p>아직 계정이 없으신가요? <a href="{{ url_for('register') }}">회원 가입</a></p>
</body>
</html>
```

## register.html (추가) 
```
<!DOCTYPE html>
<html>
<head>
    <title>회원 가입</title>
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <h1>회원 가입</h1>
    <form method="POST">
        <label for="username">사용자 이름:</label><br>
        <input type="text" id="username" name="username" required><br><br>
        <label for="password">비밀번호:</label><br>
        <input type="password" id="password" name="password" required><br><br>
        <input type="submit" value="가입">
    </form>
    <p>이미 계정이 있으신가요? <a href="{{ url_for('login') }}">로그인</a></p>
</body>
</html>
```

## .env 파일 만들기 
### SECRET_KEY 생성하기 
```
import secrets
import string

# 32바이트(256비트)의 무작위 문자열 생성
# 기본적으로 URL-safe text를 생성하지만, 더 다양한 문자를 포함할 수도 있습니다.
# secret_key = secrets.token_urlsafe(32)

# 더 복잡한 키를 위해 대소문자, 숫자, 특수문자를 포함할 수 있습니다.
alphabet = string.ascii_letters + string.digits + string.punctuation
secret_key = ''.join(secrets.choice(alphabet) for i in range(50)) # 50자리 (더 길게 해도 됨)

print(secret_key)
```

## index.html (수정) 
```
<!DOCTYPE html>
<html lang="ko">

<head>
    <meta charset="UTF-8">
    <title>회원 관리 및 일반 게시판</title> 
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>

<body>
    <header class="main-header">
        <div class="logo">경성대학교 꿀팁!</div>
        <nav class="user-auth">
            {% if current_user.is_authenticated %}
            <span>
                {% if current_user.profile_picture %}
                <img src="{{ current_user.profile_picture }}" alt="프로필 사진" class="profile-pic">
                {% endif %}
                {{ current_user.username }}님 환영합니다!
            </span>
            <a href="{{ url_for('logout') }}">로그아웃</a>
            {% else %}
            <a href="{{ url_for('login') }}">로그인</a>
            <a href="{{ url_for('register') }}">회원 가입</a>
            {% endif %}
        </nav>
    </header>

</body>

</html>
```

## style.css (수정)
```
/* 기본 스타일 초기화 */
body,
h1,
h2,
h3,
p,
ul,
li {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* --- 전역 텍스트 및 배경 스타일 --- */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f0f4f8; /* 밝은 회색 배경 */
    color: #003060;
    line-height: 1.6;
}

/* --- 헤더 스타일 (index.html에서 사용) --- */
.main-header {
    background-color: #004080; /* 메인 파란색 */
    color: white;
    padding: 10px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 1.5em;
    font-weight: bold;
}

/* --- 사용자 인증 내비게이션 링크 스타일 (index.html 헤더) --- */
.user-auth {
    display: flex;
    align-items: center;
}

.user-auth span {
    color: white;
    margin-right: 15px;
    display: inline-flex; /* 프로필 사진과 텍스트를 한 줄에 정렬 */
    align-items: center; /* 세로 중앙 정렬 */
}

.user-auth a {
    color: white;
    text-decoration: none;
    margin-left: 15px;
    padding: 5px 10px;
    border-radius: 4px;
    transition: background-color 0.3s ease; /* 호버 시 부드러운 전환 */
}

.user-auth a:hover {
    background-color: rgba(255, 255, 255, 0.2); /* 호버 시 배경색 변경 */
}

/* --- 프로필 사진 스타일 (index.html에서 사용될 경우) --- */
.profile-pic {
    width: 30px; /* 원하는 크기 */
    height: 30px;
    border-radius: 50%; /* 원형으로 만듦 */
    object-fit: cover; /* 이미지가 잘리지 않고 채워지도록 */
    vertical-align: middle;
    margin-right: 5px; /* 텍스트와의 간격 */
}

/* --- 폼 관련 스타일 (login.html, register.html에서 사용) --- */
form {
    max-width: 400px; /* 폼의 최대 너비 */
    margin: 20px auto; /* 중앙 정렬 */
    padding: 20px;
    background-color: #ffffff; /* 흰색 배경 */
    border-radius: 8px; /* 모서리 둥글게 */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 그림자 효과 */
}

h1 { /* 폼 페이지의 제목 (회원 가입, 로그인) */
    text-align: center;
    color: #004080;
    margin-bottom: 20px;
}

label {
    display: block; /* 라벨을 블록 레벨 요소로 만들어 새 줄에 표시 */
    margin-bottom: 8px; /* 라벨 아래 여백 */
    font-weight: bold; /* 글꼴 굵게 */
    color: #003060;
}

input[type="text"],
input[type="password"] {
    width: calc(100% - 20px); /* 패딩 고려한 너비 (100% - 좌우 패딩) */
    padding: 10px;
    margin-bottom: 15px; /* 입력 필드 아래 여백 */
    border: 1px solid #ccc; /* 테두리 */
    border-radius: 4px; /* 모서리 둥글게 */
    font-size: 16px;
}

/* --- 로그인/회원가입 버튼 스타일 --- */
input[type="submit"] {
    background-color: #007bff; /* 파란색 배경 */
    color: white;
    padding: 12px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer; /* 마우스 오버 시 커서 변경 */
    font-size: 18px;
    width: 100%; /* 부모 요소 너비에 맞춤 */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    transition: background-color 0.3s ease; /* 호버 시 부드러운 전환 효과 */
}

input[type="submit"]:hover {
    background-color: #0056b3; /* 호버 시 약간 더 어두운 파란색 */
}

/* --- 폼 하단의 링크 스타일 ("이미 계정이 있으신가요?" 등) --- */
p {
    text-align: center;
    margin-top: 20px;
}

p a {
    color: #007bff; /* 파란색 링크 */
    text-decoration: none; /* 밑줄 제거 */
    font-weight: bold;
}

p a:hover {
    text-decoration: underline; /* 호버 시 밑줄 표시 */
}
```

## app.py(수정) 
```
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os # os 모듈을 임포트합니다.
from dotenv import load_dotenv # load_dotenv 함수를 임포트합니다.

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

# 1. Flask 애플리케이션 인스턴스 생성
app = Flask(__name__, template_folder='templates')
# os.getenv()를 사용하여 환경 변수에서 SECRET_KEY를 가져옵니다.
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'default_fallback_key' # SECRET_KEY 환경 변수가 없으면 'default_fallback_key'를 사용 (개발용)

# 2. SQLALCHEMY_DATABASE_URI 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3. SQLAlchemy 인스턴스 초기화
db = SQLAlchemy(app)

# Flask-Login 설정
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 4. 데이터베이스 모델 정의
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # email = db.Column(db.String(120), unique=True, nullable=False) # <--- 이 줄이 주석 처리되었거나 없어야 합니다.
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# 로그인 관리 (Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 루트 페이지 (홈페이지)
@app.route('/')
def index():
    return render_template('index.html') # templates 폴더의 index.html을 렌더링합니다.


# 회원 가입 페이지
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "이미 사용 중인 사용자 이름입니다."
        new_user = User(username=username, password=hashed_password) # <--- username과 password만 전달
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

# 로그인 페이지
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))  # <--- 'index'를 'home'으로 수정
        else:
            return '로그인 실패: 사용자 이름 또는 비밀번호가 올바르지 않습니다.'
    return render_template('login.html') 

# 로그아웃 처리
@app.route('/logout')
@login_required
def logout():
    logout_user()  # 로그아웃 처리
    return redirect(url_for('index')) 

# 5. 애플리케이션 컨텍스트 내에서 데이터베이스 테이블 생성
with app.app_context():
    db.create_all()


# 6. 애플리케이션 실행
if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=8000, debug=True)  # 호스트와 포트를 지정하여 실행할 경우
```

## board.html 
```
<!DOCTYPE html>
<html>
<head>
    <title>문의 게시판</title>
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='board.css') }}">

</head>
<body>
    <div class="board-header">
    <a href="{{ url_for('index') }}" class="logo-link">
        <img src="{{ url_for('static', filename='images/logo.png') }}" alt="홈으로" class="logo-img">
    </a>
    <h1>문의 게시판</h1>
    <div class="header-actions">
        <a href="{{ url_for('new_post') }}" class="action-button">새 글 작성</a>
        <a href="{{ url_for('logout') }}" class="action-button">로그아웃</a>
    </div>
</div>

    <ul class="post-list">
        {% for post in posts %}
        <li class="post-item">
            <div class="post-info">
                <a href="{{ url_for('view_post', post_id=post.id) }}" class="post-title">{{ post.title }}</a>
                <span class="post-meta">({{ post.author.username }}, {{ post.date_posted.strftime('%Y-%m-%d %H:%M') }})</span>
            </div>
            {% if current_user == post.author %}
            <div class="post-actions">
                <a href="{{ url_for('edit_post', post_id=post.id) }}">수정</a>
                <a href="{{ url_for('delete_post', post_id=post.id) }}">삭제</a>
            </div>
            {% endif %}
        </li>
        {% endfor %}
    </ul>
</body>
```

## bulletin_board.html
```
<!DOCTYPE html>
<html lang="ko"> 
    <link rel="stylesheet" href="{{ url_for('static', filename='bulletin_board.css') }}">
<head>
    <meta charset="UTF-8">
    <title>게시판</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <h1>게시판</h1>
        <table>
            <thead>
                <tr>
                    <th>제목</th>
                    <th>작성일</th>
                </tr>
            </thead>
            <tbody>
                {% for post in posts %}
                <tr>
                    <td><a href="{{ url_for('view_bulletin_post', post_id=post.id) }}">{{ post.title }}</a></td>
                    <td>{{ post.date_posted.strftime('%Y-%m-%d %H:%M') }}</td>
                </tr>
                {% else %}
                <tr><td colspan="2">게시글이 없습니다.</td></tr>
                {% endfor %}
            </tbody>
        </table>
        {% if current_user.is_authenticated %}
        <a href="{{ url_for('new_bulletin_post') }}" class="button">새 글 쓰기</a>
        {% endif %}
        <a href="{{ url_for('index') }}">홈으로</a>
    </div>
</body>
</html>
```

## edit_post.html 
```
<!DOCTYPE html>
<html>
<head>
    <title>글 수정</title>
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <h1>글 수정</h1>
    <form method="POST">
        <label for="title">제목:</label><br>
        <input type="text" id="title" name="title" value="{{ post.title }}" required><br><br>
        <label for="content">내용:</label><br>
        <textarea id="content" name="content" rows="10" cols="80" required>{{ post.content }}</textarea><br><br>
        <input type="submit" value="수정">
    </form>
    <p><a href="{{ url_for('view_post', post_id=post.id) }}">돌아가기</a></p>
</body>
</html>
```

## new_bulletin_post.html 
```
<!DOCTYPE html>
<html lang="ko"> 
    <link rel="stylesheet" href="{{ url_for('static', filename='bulletin_board.css') }}">
<head>
    <meta charset="UTF-8">
    <title>새 글 쓰기</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <h1>새 글 쓰기</h1>
        <form method="POST">
            <label for="title">제목:</label>
            <input type="text" name="title" required><br>
            <label for="content">내용:</label>
            <textarea name="content" rows="10" required></textarea><br>
            <input type="submit" value="저장">
        </form>
        <a href="{{ url_for('bulletin_board') }}">게시판으로 돌아가기</a>
    </div>
</body>
</html>
```

## new_post.html 
```
<!DOCTYPE html>
<html>
<head>
    <title>새 글 작성</title>
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <h1>새 글 작성</h1>
    <form method="POST">
        <label for="title">제목:</label><br>
        <input type="text" id="title" name="title" required><br><br>
        <label for="content">내용:</label><br>
        <textarea id="content" name="content" rows="10" cols="80" required></textarea><br><br>
        <input type="submit" value="작성">
    </form>
    <p><a href="{{ url_for('board') }}">게시판으로 돌아가기</a></p>
</body>
</html>
```

## view_bulletin_post.html 
```
<!DOCTYPE html>
<html lang="ko">

<head>
    <meta charset="UTF-8">
    <title>{{ post.title }}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='bulletin_board.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='comments.css') }}"> </head>

<body>
    <div class="container">
        <h1>{{ post.title }}</h1>
        <p>작성일: {{ post.date_posted.strftime('%Y-%m-%d %H:%M') }}</p>
        <div class="content">
            {{ post.content }}
        </div>
        <a href="{{ url_for('bulletin_board') }}">게시판으로 돌아가기</a>

        <hr>

        <div class="comments-section">
            <h2>댓글</h2>
            {% if post.comments %}
                <ul>
                    {% for comment in post.comments %}
                    <li>
                        <strong>{{ comment.author.username }}</strong> - 
                        <small>{{ comment.date_posted.strftime('%Y-%m-%d %H:%M') }}</small><br>
                        {{ comment.content }}
                    </li>
                    {% endfor %}
                </ul>
            {% else %}
                <p>댓글이 없습니다.</p>
            {% endif %}
        </div>

        <hr>

        {% if current_user.is_authenticated %}
        <div class="comment-form">
            <h3>댓글 작성</h3>
            <form action="{{ url_for('add_bulletin_comment', post_id=post.id) }}" method="POST">
                <textarea name="content" rows="4" cols="50" placeholder="댓글 내용을 입력하세요." required></textarea><br>
                <button type="submit">작성</button>
            </form>
        </div>
        {% else %}
        <p>댓글을 작성하려면 <a href="{{ url_for('login') }}">로그인</a>하세요.</p>
        {% endif %}
    </div>
</body>

</html>
```

## view.html 
```
<!DOCTYPE html>
<html>
<head>
    <title>{{ post.title }}</title>
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='comments.css') }}">
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='view.css') }}">
</head>
<body>
    <div class="view-container">
        <h1 class="post-title">{{ post.title }}</h1>
        <div class="post-meta">
            <span class="meta-line">작성자: {{ post.author.username }}</span>
            <span class="meta-line">작성일: {{ post.date_posted.strftime('%Y-%m-%d %H:%M:%S') }}</span>
        </div>

        <div class="content">
            {{ post.content|replace('\n', '<br>')|safe }}
        </div>

        <p><a href="{{ url_for('board') }}" class="back-link">← 게시판으로 돌아가기</a></p>

        {% if current_user.is_authenticated and current_user == post.author %}
            <div class="post-actions">
                <a href="{{ url_for('edit_post', post_id=post.id) }}">수정</a> |
                <a href="{{ url_for('delete_post', post_id=post.id) }}" onclick="return confirm('정말로 삭제하시겠습니까?')">삭제</a>
            </div>
        {% endif %}

        <h2 class="comments-title">댓글</h2> {# 클래스 추가 #}
        {% if post.comments %}
            <ul class="comment-list">
                {% for comment in post.comments %}
                    <li>
                        <strong>{{ comment.author.username }}</strong> ({{ comment.date_posted.strftime('%Y-%m-%d %H:%M:%S') }}):
                        <div class="comment-content">
                            {{ comment.content|replace('\n', '<br>')|safe }}
                        </div>
                    </li>
                {% endfor %}
            </ul>
        {% else %}
            <p class="no-comments-message">아직 댓글이 없습니다.</p> {# 클래스 추가 #}
        {% endif %}

        {% if current_user.is_authenticated %}
            <h3 class="comment-form-title">댓글 작성</h3> {# 클래스 추가 #}
            <form method="POST" action="{{ url_for('add_comment', post_id=post.id) }}" class="comment-form">
                <textarea name="content" rows="5" required></textarea><br>
                <input type="submit" value="댓글 작성">
            </form>
        {% else %}
            <p><a href="{{ url_for('login') }}">로그인</a> 후 댓글을 작성할 수 있습니다.</p>
        {% endif %}
    </div>
</body>
</html>
``` 








































# 전체 코드 (자세한 주석이 달린 버전)
# static 

### board.css 
```
/*
    이 CSS 파일은 웹사이트의 게시판 관련 요소들의 시각적인 스타일을 정의합니다.
    게시글 목록, 개별 게시글 상세 페이지, 그리고 특히 **댓글 섹션**과 **댓글 작성 폼**에 대한 디자인을 담당합니다.
    각 CSS 규칙은 특정 HTML 요소나 클래스에 어떤 스타일을 적용할지 명확하게 설명합니다.
*/

/* comments-section 전체에 대한 스타일 */
.comments-section {
    margin-top: 20px; /* 상단에 20픽셀의 외부 여백을 설정하여 다른 요소와 분리합니다. */
    padding: 15px; /* 내부적으로 15픽셀의 여백(패딩)을 추가합니다. */
    border: 1px solid #e0e0e0; /* 1픽셀 두께의 연한 회색 실선 테두리를 추가합니다. */
    border-radius: 8px; /* 테두리 모서리를 8픽셀 둥글게 만들어 부드러운 느낌을 줍니다. */
    background-color: #f9f9f9; /* 섹션의 배경색을 아주 연한 회색으로 설정하여 가시성을 높입니다. */
}

/* 댓글 섹션 제목 (<h2>) 스타일 */
.comments-section h2 {
    font-size: 1.5em; /* 기본 글꼴 크기의 1.5배로 설정하여 제목임을 강조합니다. */
    color: #333; /* 글자색을 진한 회색(#333)으로 설정합니다. */
    margin-bottom: 15px; /* 제목 아래에 15픽셀의 외부 여백을 설정합니다. */
    border-bottom: 2px solid #eee; /* 2픽셀 두께의 아주 연한 회색 실선 하단 테두리를 추가합니다. */
    padding-bottom: 10px; /* 하단 테두리 위에 10픽셀의 내부 여백을 주어 텍스트와 테두리 사이의 공간을 확보합니다. */
}

/* 댓글 목록 (<ul>) 스타일 */
.comments-section ul {
    list-style: none; /* 목록 항목의 기본 마커(예: 불릿 기호)를 제거합니다. */
    padding: 0; /* 목록의 내부 여백(패딩)을 제거합니다. */
    margin: 0; /* 목록의 외부 여백(마진)을 제거합니다. */
}

/* 개별 댓글 (<li>) 스타일 */
.comments-section ul li {
    background-color: #fff; /* 개별 댓글 항목의 배경색을 흰색으로 설정합니다. */
    border: 1px solid #ddd; /* 1픽셀 두께의 연한 회색 실선 테두리를 추가합니다. */
    border-radius: 5px; /* 테두리 모서리를 5픽셀 둥글게 만듭니다. */
    padding: 10px 15px; /* 상하 10픽셀, 좌우 15픽셀의 내부 여백을 설정합니다. */
    margin-bottom: 10px; /* 각 댓글 항목 사이에 10픽셀의 하단 외부 여백을 추가합니다. */
    box-shadow: 0 2px 4px rgba(0,0,0,0.05); /* 약간의 그림자 효과를 추가하여 입체감을 줍니다. (가로 0, 세로 2, 블러 4, 색상 투명도 5%) */
}

/* 마지막 댓글 항목 (<li>)에 대한 특별 스타일 */
.comments-section ul li:last-child {
    margin-bottom: 0; /* 목록의 마지막 댓글 항목에는 하단 여백을 제거하여 깔끔하게 마무리합니다. */
}

/* 댓글 작성자 이름 (<strong>) 스타일 */
.comments-section ul li strong {
    color: #007bff; /* 작성자 이름을 밝은 파란색(#007bff)으로 강조합니다. */
    font-weight: bold; /* 글꼴 두께를 굵게 설정합니다. */
}

/* 댓글 작성일자 (<small>) 스타일 */
.comments-section ul li small {
    color: #888; /* 작성일자 글자색을 회색(#888)으로 설정합니다. */
    font-size: 0.85em; /* 글꼴 크기를 기본 글꼴 크기의 85%로 줄여서 보조적인 정보임을 나타냅니다. */
    margin-left: 10px; /* 작성자 이름으로부터 10픽셀의 왼쪽 외부 여백을 줍니다. */
}

/* 댓글 내용 (주로 <p> 태그 안에 있을 것으로 예상) 스타일 */
/*
    주의: 이 선택자는 ".comments-section ul li"만으로 지정되어 있어서,
    해당 `<li>` 요소 자체의 스타일이거나, `<li>` 안에 직접 텍스트가 있을 경우 적용됩니다.
    만약 댓글 내용이 `<p>` 태그 내에 있다면 `.comments-section ul li p`로
    선택자를 더 명확히 지정하는 것이 좋습니다.
*/
.comments-section ul li {
    line-height: 1.6; /* 줄 간격을 1.6배로 설정하여 가독성을 높입니다. */
    color: #555; /* 글자색을 중간 회색(#555)으로 설정합니다. */
    white-space: pre-wrap; /* 공백 문자와 줄 바꿈을 HTML에 작성된 그대로 유지하면서, 필요한 경우 줄 바꿈을 허용합니다. (예: 여러 줄의 텍스트) */
    word-wrap: break-word; /* 긴 단어가 컨테이너를 벗어나는 경우 단어를 끊어서 줄 바꿈합니다. */
}

/* 댓글이 없을 때의 메시지 (<p> 또는 특정 클래스) 스타일 */
/*
    주의: 이 선택자는 `.comments-section p`로, 댓글 목록 외의 다른 `<p>` 태그에도
    영향을 줄 수 있습니다. 만약 댓글이 없을 때의 메시지에만 적용하려면
    `.comments-section .no-comments-message`와 같이 특정 클래스를 사용하는 것이 더 명확합니다.
*/
.comments-section p {
    color: #777; /* 글자색을 회색(#777)으로 설정합니다. */
    text-align: center; /* 텍스트를 중앙 정렬합니다. */
    padding: 20px; /* 내부 여백(패딩)을 20픽셀로 설정합니다. */
    background-color: #f0f0f0; /* 배경색을 연한 회색(#f0f0f0)으로 설정합니다. */
    border-radius: 5px; /* 모서리를 5픽셀 둥글게 만듭니다. */
}

/* 댓글 작성 폼 (comment-form) 스타일 */
.comment-form {
    margin-top: 30px; /* 상단에 30픽셀의 외부 여백을 설정하여 댓글 목록과 명확히 구분합니다. */
    padding: 20px; /* 내부적으로 20픽셀의 여백(패딩)을 추가합니다. */
    border: 1px solid #e0e0e0; /* 1픽셀 두께의 연한 회색 실선 테두리를 추가합니다. */
    border-radius: 8px; /* 테두리 모서리를 8픽셀 둥글게 만듭니다. */
    background-color: #f9f9f9; /* 배경색을 아주 연한 회색으로 설정합니다. */
}

/* 댓글 작성 폼 제목 (<h3>) 스타일 */
.comment-form h3 {
    font-size: 1.3em; /* 기본 글꼴 크기의 1.3배로 설정하여 제목임을 나타냅니다. */
    color: #333; /* 글자색을 진한 회색(#333)으로 설정합니다. */
    margin-bottom: 15px; /* 제목 아래에 15픽셀의 외부 여백을 설정합니다. */
}

/* 댓글 입력란 (<textarea>) 스타일 */
.comment-form textarea {
    width: 100%; /* 부모 요소의 전체 너비를 차지하도록 설정합니다. */
    padding: 10px; /* 내부적으로 10픽셀의 여백(패딩)을 추가합니다. */
    border: 1px solid #ccc; /* 1픽셀 두께의 연한 회색 실선 테두리를 추가합니다. */
    border-radius: 5px; /* 테두리 모서리를 5픽셀 둥글게 만듭니다. */
    box-sizing: border-box; /* 패딩과 테두리가 요소의 전체 너비에 포함되도록 계산 방식을 변경합니다. (레이아웃 계산을 편리하게 함) */
    margin-bottom: 10px; /* 입력란 아래에 10픽셀의 외부 여백을 설정합니다. */
    resize: vertical; /* 사용자가 세로 방향으로만 입력란의 크기를 조절할 수 있도록 허용합니다. */
    min-height: 80px; /* 입력란의 최소 높이를 80픽셀로 설정합니다. */
}

/* 댓글 제출 버튼 (<button>) 스타일 */
.comment-form button {
    background-color: #007bff; /* 버튼의 배경색을 밝은 파란색(#007bff)으로 설정합니다. */
    color: white; /* 버튼의 글자색을 흰색으로 설정합니다. */
    padding: 10px 20px; /* 상하 10픽셀, 좌우 20픽셀의 내부 여백을 설정합니다. */
    border: none; /* 버튼의 테두리를 제거합니다. */
    border-radius: 5px; /* 테두리 모서리를 5픽셀 둥글게 만듭니다. */
    cursor: pointer; /* 마우스 커서를 포인터 모양으로 변경하여 클릭 가능함을 나타냅니다. */
    font-size: 1em; /* 글꼴 크기를 기본 글꼴 크기와 동일하게 설정합니다. */
    transition: background-color 0.3s ease; /* 배경색 변경 시 0.3초 동안 부드러운 전환 효과를 적용하여 사용자 경험을 향상시킵니다. */
}

/* 버튼에 마우스 오버 시 (hover) 스타일 */
.comment-form button:hover {
    background-color: #0056b3; /* 마우스 커서가 버튼 위에 올라갔을 때 배경색을 더 진한 파란색(#0056b3)으로 변경합니다. */
}
```

### bulletin_board.css 
```
/*
    bulletin_board.css 파일은 웹사이트의 게시판 관련 페이지들(게시글 목록, 새 글 쓰기, 게시글 상세 보기)의
    전반적인 시각적 스타일을 정의합니다.
    여기에는 공통적인 컨테이너 스타일부터 테이블 레이아웃, 버튼 디자인, 폼 요소,
    그리고 댓글 섹션에 이르기까지 다양한 요소에 대한 스타일 규칙이 포함됩니다.
*/

/* --- 게시판 전체 목록 스타일 (bulletin_board.html) --- */

/* '.container' 클래스는 게시판 페이지의 주요 콘텐츠를 감싸는 컨테이너의 스타일을 정의합니다.
   게시글 목록, 새 글 쓰기 폼, 게시글 상세 페이지 등 여러 페이지에서 공통적으로 사용될 수 있습니다. */
.container {
    max-width: 800px; /* 컨테이너의 최대 너비를 800픽셀로 제한하여 너무 넓게 퍼지는 것을 방지합니다. */
    margin: 20px auto; /* 상하로 20픽셀의 외부 여백을 주고, 좌우는 'auto'로 설정하여 컨테이너를 페이지 중앙에 배치합니다. */
    padding: 20px; /* 컨테이너 내부적으로 20픽셀의 여백(패딩)을 추가합니다. */
    background-color: #fff; /* 컨테이너의 배경색을 흰색으로 설정합니다. */
    border: 1px solid #ddd; /* 1픽셀 두께의 연한 회색 실선 테두리를 추가합니다. */
    border-radius: 5px; /* 테두리 모서리를 5픽셀 둥글게 만들어 부드러운 느낌을 줍니다. */
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* 약간의 그림자 효과를 추가하여 컨테이너에 입체감을 줍니다.
                                                  (가로 오프셋 0, 세로 오프셋 2, 블러 반경 5, 색상 투명도 10%) */
}

/* '.container' 내부의 <h1> 태그 (페이지 제목) 스타일 */
.container h1 {
    color: #007bff; /* 제목의 글자색을 밝은 파란색(#007bff)으로 설정합니다. */
    margin-bottom: 20px; /* 제목 아래에 20픽셀의 외부 여백을 설정합니다. */
    text-align: center; /* 텍스트를 중앙 정렬합니다. */
}

/* '.container' 내부의 <table> 태그 (게시글 목록 테이블) 스타일 */
.container table {
    width: 100%; /* 테이블 너비를 부모 요소(컨테이너)에 꽉 채우도록 설정합니다. */
    border-collapse: collapse; /* 테이블 셀 사이의 경계를 단일 선으로 병합하여 깔끔하게 만듭니다. */
    margin-bottom: 20px; /* 테이블 아래에 20픽셀의 외부 여백을 설정합니다. */
}

/* '.container' 내부의 <th> (테이블 헤더)와 <td> (테이블 데이터) 셀 스타일 */
.container th, .container td {
    border-bottom: 1px solid #eee; /* 각 셀의 하단에 1픽셀 두께의 아주 연한 회색 실선 테두리를 추가하여 행을 구분합니다. */
    padding: 10px; /* 셀 내부적으로 10픽셀의 여백(패딩)을 추가합니다. */
    text-align: left; /* 셀 안의 텍스트를 왼쪽 정렬합니다. */
}

/* '.container' 내부의 <th> (테이블 헤더) 셀에 대한 추가 스타일 */
.container th {
    background-color: #f8f9fa; /* 테이블 헤더의 배경색을 매우 연한 회색으로 설정합니다. */
    font-weight: bold; /* 헤더 텍스트의 글꼴 두께를 굵게 설정합니다. */
}

/* '.container' 내부의 <tbody> (테이블 본문) 내 각 행 (<tr>)에 마우스 오버 시 스타일 */
.container tbody tr:hover {
    background-color: #f5f5f5; /* 마우스 커서가 행 위에 올라갔을 때 배경색을 연한 회색으로 변경하여 선택 효과를 줍니다. */
}

/* '.container' 내부의 <tbody> (테이블 본문) 내 <td> (테이블 데이터) 안의 <a> 태그 (게시글 제목 링크) 스타일 */
.container tbody td a {
    text-decoration: none; /* 링크의 밑줄을 제거합니다. */
    color: #333; /* 링크의 글자색을 진한 회색(#333)으로 설정합니다. */
}

/* '.container' 내부의 <tbody> 내 <td> 안의 <a> 태그에 마우스 오버 시 스타일 */
.container tbody td a:hover {
    color: #007bff; /* 마우스 오버 시 링크의 글자색을 밝은 파란색(#007bff)으로 변경합니다. */
    text-decoration: underline; /* 마우스 오버 시 링크에 밑줄을 다시 추가합니다. */
}

/* '.container' 내부의 '.button' 클래스 (버튼 공통 스타일) */
.container .button {
    display: inline-block; /* 요소를 인라인-블록 레벨로 표시하여 가로로 나열되면서 너비/높이 설정이 가능하게 합니다. */
    padding: 10px 15px; /* 상하 10픽셀, 좌우 15픽셀의 내부 여백을 설정합니다. */
    background-color: #007bff; /* 버튼의 배경색을 밝은 파란색(#007bff)으로 설정합니다. */
    color: white; /* 버튼의 글자색을 흰색으로 설정합니다. */
    border: none; /* 버튼의 테두리를 제거합니다. */
    border-radius: 5px; /* 테두리 모서리를 5픽셀 둥글게 만듭니다. */
    text-decoration: none; /* 링크의 밑줄을 제거합니다 (버튼이 <a> 태그일 경우). */
    cursor: pointer; /* 마우스 커서를 포인터 모양으로 변경하여 클릭 가능함을 나타냅니다. */
    margin-right: 10px; /* 오른쪽에 10픽셀의 외부 여백을 주어 다른 버튼과 분리합니다. */
}

/* '.container' 내부의 '.button' 클래스에 마우스 오버 시 스타일 */
.container .button:hover {
    background-color: #0056b3; /* 마우스 오버 시 배경색을 더 진한 파란색(#0056b3)으로 변경합니다. */
}

/* '.container' 내부의 일반적인 <a> 태그 (기타 링크) 스타일 */
.container a {
    color: #007bff; /* 링크의 글자색을 밝은 파란색(#007bff)으로 설정합니다. */
    text-decoration: none; /* 링크의 밑줄을 제거합니다. */
}

/* '.container' 내부의 일반적인 <a> 태그에 마우스 오버 시 스타일 */
.container a:hover {
    text-decoration: underline; /* 마우스 오버 시 링크에 밑줄을 추가합니다. */
}

/* --- 새 글 쓰기 폼 스타일 (new_bulletin_post.html) --- */

/* '.container' 내부의 <form> 태그 안의 <label> 태그 (폼 필드 라벨) 스타일 */
.container form label {
    display: block; /* 라벨을 블록 레벨 요소로 만들어 다음 요소가 새 줄에서 시작하도록 합니다. */
    margin-bottom: 5px; /* 라벨 아래에 5픽셀의 외부 여백을 설정합니다. */
    font-weight: bold; /* 글꼴 두께를 굵게 설정합니다. */
    color: #555; /* 글자색을 중간 회색(#555)으로 설정합니다. */
}

/* '.container' 내부의 <form> 태그 안의 텍스트 입력 필드 (<input type="text">)와 텍스트 영역 (<textarea>) 스타일 */
.container form input[type="text"],
.container form textarea {
    width: 100%; /* 너비를 부모 요소에 꽉 채우도록 설정합니다. */
    padding: 10px; /* 내부적으로 10픽셀의 여백(패딩)을 추가합니다. */
    margin-bottom: 15px; /* 아래에 15픽셀의 외부 여백을 설정합니다. */
    border: 1px solid #ccc; /* 1픽셀 두께의 연한 회색 실선 테두리를 추가합니다. */
    border-radius: 4px; /* 테두리 모서리를 4픽셀 둥글게 만듭니다. */
    box-sizing: border-box; /* 패딩과 테두리가 요소의 전체 너비에 포함되도록 계산 방식을 변경합니다. */
    font-size: 1em; /* 글꼴 크기를 기본 글꼴 크기와 동일하게 설정합니다. */
}

/* '.container' 내부의 <form> 태그 안의 <textarea> (텍스트 영역)에 대한 추가 스타일 */
.container form textarea {
    resize: vertical; /* 사용자가 세로 방향으로만 텍스트 영역의 크기를 조절할 수 있도록 허용합니다. */
    min-height: 150px; /* 텍스트 영역의 최소 높이를 150픽셀로 설정합니다. */
}

/* '.container' 내부의 <form> 태그 안의 제출 버튼 (<input type="submit">) 스타일 */
.container form input[type="submit"] {
    background-color: #28a745; /* 버튼의 배경색을 녹색(#28a745)으로 설정합니다. */
    color: white; /* 버튼의 글자색을 흰색으로 설정합니다. */
    padding: 10px 15px; /* 상하 10픽셀, 좌우 15픽셀의 내부 여백을 설정합니다. */
    border: none; /* 버튼의 테두리를 제거합니다. */
    border-radius: 5px; /* 테두리 모서리를 5픽셀 둥글게 만듭니다. */
    cursor: pointer; /* 마우스 커서를 포인터 모양으로 변경하여 클릭 가능함을 나타냅니다. */
    font-size: 1em; /* 글꼴 크기를 기본 글꼴 크기와 동일하게 설정합니다. */
}

/* '.container' 내부의 <form> 태그 안의 제출 버튼에 마우스 오버 시 스타일 */
.container form input[type="submit"]:hover {
    background-color: #218838; /* 마우스 오버 시 배경색을 더 진한 녹색(#218838)으로 변경합니다. */
}

/* --- 게시글 상세 페이지 스타일 (view_bulletin_post.html) --- */

/* '.container' 내부의 '.content' 클래스 (게시글 본문 내용) 스타일 */
.container .content {
    padding: 15px 0; /* 상하 15픽셀, 좌우 0픽셀의 내부 여백을 설정합니다. */
    border-top: 1px solid #eee; /* 상단에 1픽셀 두께의 아주 연한 회색 실선 테두리를 추가합니다. */
    border-bottom: 1px solid #eee; /* 하단에 1픽셀 두께의 아주 연한 회색 실선 테두리를 추가합니다. */
    margin-bottom: 20px; /* 본문 내용 아래에 20픽셀의 외부 여백을 설정합니다. */
    line-height: 1.6; /* 줄 간격을 1.6배로 설정하여 가독성을 높입니다. */
}

/* '.container' 내부의 '.content' 클래스 안의 <p> 태그 (게시글 단락) 스타일 */
.container .content p {
    margin-bottom: 10px; /* 각 단락 아래에 10픽셀의 외부 여백을 설정합니다. */
}

/* '.container' 내부의 '.date' 클래스 (게시글 작성일자) 스타일 */
.container .date {
    color: #777; /* 글자색을 회색(#777)으로 설정합니다. */
    font-size: 0.9em; /* 글꼴 크기를 기본 글꼴 크기의 90%로 줄여서 보조적인 정보임을 나타냅니다. */
    margin-bottom: 10px; /* 날짜 아래에 10픽셀의 외부 여백을 설정합니다. */
}

/* --- 댓글 섹션 (게시글 상세 페이지의 댓글 영역) --- */

/* '.comment-section' 클래스 (전체 댓글 섹션 컨테이너) 스타일 */
.comment-section {
    margin-top: 40px; /* 상단에 40픽셀의 외부 여백을 설정하여 게시글 본문과 충분히 구분합니다. */
    padding: 20px; /* 내부적으로 20픽셀의 여백(패딩)을 추가합니다. */
    background-color: #ffffff; /* 배경색을 흰색으로 설정합니다. */
    border: 1px solid #a8c7e7; /* 1픽셀 두께의 연한 파란색 계열 실선 테두리를 추가합니다. */
    border-radius: 5px; /* 테두리 모서리를 5픽셀 둥글게 만듭니다. */
}

/* '.comment-section' 내부의 <h2> 태그 (댓글 섹션 제목) 스타일 */
.comment-section h2 {
    color: #004080; /* 제목의 글자색을 진한 파란색(#004080)으로 설정합니다. */
    margin-bottom: 15px; /* 제목 아래에 15픽셀의 외부 여백을 설정합니다. */
    border-bottom: 2px solid #a8c7e7; /* 2픽셀 두께의 연한 파란색 계열 실선 하단 테두리를 추가합니다. */
    padding-bottom: 5px; /* 하단 테두리 위에 5픽셀의 내부 여백을 주어 텍스트와 테두리 사이 공간을 확보합니다. */
}

/* '.comments' 클래스 (댓글 목록을 감싸는 요소) 내부의 '.comment' 클래스 (개별 댓글 항목) 스타일 */
.comments .comment {
    margin-bottom: 15px; /* 각 댓글 항목 아래에 15픽셀의 외부 여백을 설정합니다. */
    padding-bottom: 10px; /* 내부적으로 하단에 10픽셀의 여백(패딩)을 추가합니다. */
    border-bottom: 1px solid #d0dbe8; /* 하단에 1픽셀 두께의 연한 파란색 계열 실선 테두리를 추가하여 각 댓글을 구분합니다. */
}

/* '.comment' 클래스 내부의 <textarea> 태그 (댓글 입력란) 스타일 */
.comment textarea {
    width: 100%; /* 너비를 부모 요소에 꽉 채우도록 설정합니다. */
    padding: 10px; /* 내부적으로 10픽셀의 여백(패딩)을 추가합니다. */
    border: 1px solid #a8c7e7; /* 1픽셀 두께의 연한 파란색 계열 실선 테두리를 추가합니다. */
    border-radius: 3px; /* 테두리 모서리를 3픽셀 둥글게 만듭니다. */
    background-color: #f0f4f8; /* 배경색을 아주 연한 파란색(#f0f4f8)으로 설정하여 입력 가능한 영역임을 시각적으로 나타냅니다. */
    resize: vertical; /* 사용자가 세로 방향으로만 크기를 조절할 수 있도록 허용합니다. */
    margin-bottom: 10px; /* 입력란 아래에 10픽셀의 외부 여백을 설정합니다. */
}

/* '.comment-section' 내부의 <button> 태그 (댓글 제출 버튼) 스타일 */
.comment-section button {
    background-color: #004080; /* 버튼의 배경색을 진한 파란색(#004080)으로 설정합니다. */
    color: white; /* 버튼의 글자색을 흰색으로 설정합니다. */
    border: none; /* 버튼의 테두리를 제거합니다. */
    padding: 8px 12px; /* 상하 8픽셀, 좌우 12픽셀의 내부 여백을 설정합니다. */
    border-radius: 3px; /* 테두리 모서리를 3픽셀 둥글게 만듭니다. */
    cursor: pointer; /* 마우스 커서를 포인터 모양으로 변경하여 클릭 가능함을 나타냅니다. */
}

/* '.comment-section' 내부의 <button> 태그에 마우스 오버 시 스타일 */
.comment-section button:hover {
    background-color: #003060; /* 마우스 오버 시 배경색을 더 진한 파란색(#003060)으로 변경합니다. */
}
```

### comments.css 
```
/*
    comments.css 파일은 웹사이트의 댓글 섹션에 대한 모든 시각적 스타일을 정의합니다.
    이 스타일시트는 댓글 목록, 개별 댓글 항목, 댓글 작성자 정보, 댓글 내용,
    그리고 댓글 작성 폼에 이르기까지 댓글과 관련된 다양한 HTML 요소들의 디자인을 제어합니다.
    특히, `view.html`이나 `view_bulletin_post.html`과 같은 파일에서 사용될 수 있도록
    유연한 선택자들을 포함하고 있습니다.
*/

/* 댓글 섹션 전체에 대한 스타일 */
/*
    이 규칙은 `.comments-section` 클래스를 가진 요소, `<h2>댓글</h2>` 바로 뒤에 오는
    `ul.comment-list` 요소, 그리고 `.comment-form` 클래스를 가진 요소에 공통적으로 적용됩니다.
    이는 HTML 구조에 따라 다양한 방식으로 댓글 섹션을 감싸는 요소들을 타겟팅하기 위함입니다.
*/
.comments-section, h2 + .comment-list, .comment-form {
    margin-top: 20px; /* 상단에 20픽셀의 외부 여백을 설정하여 다른 섹션과 구분합니다. */
    padding: 15px; /* 내부적으로 15픽셀의 여백(패딩)을 추가하여 콘텐츠와 테두리 사이에 공간을 만듭니다. */
    border: 1px solid #e0e0e0; /* 1픽셀 두께의 연한 회색 실선 테두리를 추가합니다. */
    border-radius: 8px; /* 테두리 모서리를 8픽셀 둥글게 만들어 부드러운 느낌을 줍니다. */
    background-color: #f9f9f9; /* 배경색을 아주 연한 회색으로 설정하여 섹션을 시각적으로 강조합니다. */
}

/* 댓글 섹션 제목 스타일 */
/*
    이 규칙은 `.comments-section` 내부의 `<h2>` 태그와 `h2.comments-title` 클래스를 가진 `<h2>` 태그에 적용됩니다.
    주로 "댓글"과 같은 섹션 제목의 스타일을 정의합니다.
*/
.comments-section h2, h2.comments-title {
    font-size: 1.5em; /* 기본 글꼴 크기의 1.5배로 설정하여 제목임을 명확히 합니다. */
    color: #333; /* 글자색을 진한 회색(#333)으로 설정합니다. */
    margin-bottom: 15px; /* 제목 아래에 15픽셀의 외부 여백을 설정합니다. */
    border-bottom: 2px solid #eee; /* 2픽셀 두께의 아주 연한 회색 실선 하단 테두리를 추가하여 제목 아래에 구분선을 만듭니다. */
    padding-bottom: 10px; /* 하단 테두리 위에 10픽셀의 내부 여백을 주어 텍스트와 구분선 사이의 공간을 확보합니다. */
}

/* 댓글 목록 (ul) 스타일 */
/*
    이 규칙은 `.comments-section` 내부의 `<ul>` 태그와 `.comment-list` 클래스를 가진 `<ul>` 태그에 적용됩니다.
    댓글들이 나열되는 목록 전체의 스타일을 정의합니다.
*/
.comments-section ul, .comment-list {
    list-style: none; /* 목록 항목의 기본 마커(예: 불릿 기호)를 제거하여 깔끔하게 만듭니다. */
    padding: 0; /* 목록의 내부 여백(패딩)을 제거하여 콘텐츠가 컨테이너 가장자리에 붙도록 합니다. */
    margin: 0; /* 목록의 외부 여백(마진)을 제거하여 불필요한 공간을 없앱니다. */
}

/* 개별 댓글 (li) 스타일 */
/*
    이 규칙은 `.comments-section` 내부의 `<ul>` 태그 안의 `<li>` 태그와 `.comment-list` 클래스를 가진 `<ul>` 태그 안의 `<li>` 태그에 적용됩니다.
    각각의 개별 댓글 항목에 대한 스타일을 정의합니다.
*/
.comments-section ul li, .comment-list li {
    background-color: #fff; /* 개별 댓글 항목의 배경색을 흰색으로 설정하여 가독성을 높입니다. */
    border: 1px solid #ddd; /* 1픽셀 두께의 연한 회색 실선 테두리를 추가합니다. */
    border-radius: 5px; /* 테두리 모서리를 5픽셀 둥글게 만들어 부드러운 느낌을 줍니다. */
    padding: 10px 15px; /* 상하 10픽셀, 좌우 15픽셀의 내부 여백을 설정합니다. */
    margin-bottom: 10px; /* 각 댓글 항목 사이에 10픽셀의 하단 외부 여백을 추가하여 구분합니다. */
    box-shadow: 0 2px 4px rgba(0,0,0,0.05); /* 약한 그림자 효과를 추가하여 항목에 입체감을 줍니다.
                                               (가로 오프셋 0, 세로 오프셋 2, 블러 반경 4, 색상 투명도 5%) */
}

/* 마지막 개별 댓글 (li) 스타일 */
/*
    이 규칙은 댓글 목록의 마지막 `<li>` 항목에만 적용됩니다.
*/
.comments-section ul li:last-child, .comment-list li:last-child {
    margin-bottom: 0; /* 마지막 댓글 항목의 하단 외부 여백을 제거하여 목록의 끝을 깔끔하게 정리합니다. */
}

/* 댓글 작성자 이름 스타일 */
/*
    이 규칙은 개별 댓글 항목 내의 `<strong>` 태그에 적용되며, 주로 작성자 이름을 나타내는 데 사용됩니다.
*/
.comments-section ul li strong, .comment-list li strong {
    color: #007bff; /* 작성자 이름을 밝은 파란색(#007bff)으로 강조합니다. */
    font-weight: bold; /* 글꼴 두께를 굵게 설정하여 시각적으로 더 돋보이게 합니다. */
}

/* 댓글 작성일자 스타일 */
/*
    이 규칙은 개별 댓글 항목 내의 `<small>` 태그에 적용되며, 주로 댓글 작성 시간을 나타내는 데 사용됩니다.
*/
.comments-section ul li small, .comment-list li small {
    color: #888; /* 작성일자의 글자색을 회색(#888)으로 설정하여 보조적인 정보임을 나타냅니다. */
    font-size: 0.85em; /* 글꼴 크기를 기본 글꼴 크기의 85%로 줄여서 작은 글씨로 표시합니다. */
    margin-left: 10px; /* 작성자 이름으로부터 10픽셀의 왼쪽 외부 여백을 줍니다. */
}

/* 댓글 내용 스타일 */
/*
    이 규칙은 개별 댓글 항목 내의 `.comment-content` 클래스를 가진 요소와,
    `.comments-section ul li` (즉, `<li>` 요소 자체)에 적용됩니다.
    이는 댓글 내용이 `<p>` 태그 등으로 감싸져 있지 않고 `<li>` 바로 아래에 텍스트로 존재할 수 있는 경우를 고려한 것입니다.
*/
.comments-section ul li .comment-content, .comment-list li .comment-content,
.comments-section ul li {
    line-height: 1.6; /* 줄 간격을 1.6배로 설정하여 텍스트의 가독성을 높입니다. */
    color: #555; /* 글자색을 중간 회색(#555)으로 설정합니다. */
    white-space: pre-wrap; /* HTML에 작성된 공백 문자(스페이스, 탭)와 줄 바꿈을 그대로 유지하면서, 필요한 경우 줄 바꿈을 허용합니다.
                               이는 긴 텍스트가 컨테이너를 벗어나지 않도록 하고, 사용자 입력 형식을 보존할 때 유용합니다. */
    word-wrap: break-word; /* 긴 단어가 컨테이너의 너비를 초과할 경우, 단어를 끊어서 줄 바꿈하도록 설정합니다. */
}

/* 댓글이 없을 때의 메시지 스타일 */
/*
    이 규칙은 `.comments-section` 내부의 `<p>` 태그와 `p.no-comments-message` 클래스를 가진 `<p>` 태그에 적용됩니다.
    주로 "댓글이 없습니다."와 같은 메시지를 표시할 때 사용됩니다.
*/
.comments-section p, p.no-comments-message {
    color: #777; /* 글자색을 회색(#777)으로 설정합니다. */
    text-align: center; /* 텍스트를 중앙 정렬합니다. */
    padding: 20px; /* 내부적으로 20픽셀의 여백(패딩)을 추가합니다. */
    background-color: #f0f0f0; /* 배경색을 아주 연한 회색(#f0f0f0)으로 설정합니다. */
    border-radius: 5px; /* 모서리를 5픽셀 둥글게 만듭니다. */
}

/* 댓글 작성 폼 (comment-form) 스타일 */
/*
    이 규칙은 `.comment-form` 클래스를 가진 요소에 적용되며, 댓글을 작성하는 입력 필드와 버튼을 포함하는 영역입니다.
*/
.comment-form {
    margin-top: 30px; /* 상단에 30픽셀의 외부 여백을 설정하여 댓글 목록과 명확히 구분합니다. */
    padding: 20px; /* 내부적으로 20픽셀의 여백(패딩)을 추가합니다. */
    border: 1px solid #e0e0e0; /* 1픽셀 두께의 연한 회색 실선 테두리를 추가합니다. */
    border-radius: 8px; /* 테두리 모서리를 8픽셀 둥글게 만듭니다. */
    background-color: #f9f9f9; /* 배경색을 아주 연한 회색으로 설정합니다. */
}

/* 댓글 작성 폼 제목 (<h3>) 스타일 */
/*
    이 규칙은 `.comment-form` 내부의 `<h3>` 태그에 적용됩니다.
    주로 "댓글 작성"과 같은 폼의 제목을 나타냅니다.
*/
.comment-form h3 {
    font-size: 1.3em; /* 기본 글꼴 크기의 1.3배로 설정하여 제목임을 나타냅니다. */
    color: #333; /* 글자색을 진한 회색(#333)으로 설정합니다. */
    margin-bottom: 15px; /* 제목 아래에 15픽셀의 외부 여백을 설정합니다. */
}

/* 댓글 입력란 (<textarea>) 스타일 */
/*
    이 규칙은 `.comment-form` 내부의 `<textarea>` 태그에 적용됩니다.
    사용자가 댓글 내용을 입력하는 필드에 대한 스타일을 정의합니다.
*/
.comment-form textarea {
    width: 100%; /* 너비를 부모 요소에 꽉 채우도록 설정합니다. */
    padding: 10px; /* 내부적으로 10픽셀의 여백(패딩)을 추가합니다. */
    border: 1px solid #ccc; /* 1픽셀 두께의 연한 회색 실선 테두리를 추가합니다. */
    border-radius: 5px; /* 테두리 모서리를 5픽셀 둥글게 만듭니다. */
    box-sizing: border-box; /* 패딩과 테두리가 요소의 전체 너비에 포함되도록 계산 방식을 변경합니다.
                               이는 너비가 100%일 때 패딩과 테두리 때문에 요소가 부모를 벗어나는 것을 방지합니다. */
    margin-bottom: 10px; /* 입력란 아래에 10픽셀의 외부 여백을 설정합니다. */
    resize: vertical; /* 사용자가 세로 방향으로만 입력란의 크기를 조절할 수 있도록 허용합니다. */
    min-height: 80px; /* 입력란의 최소 높이를 80픽셀로 설정하여 충분한 입력 공간을 제공합니다. */
}

/* 댓글 제출 버튼 (<button> 또는 <input type="submit">) 스타일 */
/*
    이 규칙은 `.comment-form` 내부의 `<button>` 태그와 `input[type="submit"]` 태그에 공통적으로 적용됩니다.
    댓글 작성을 완료하고 제출하는 버튼에 대한 스타일을 정의합니다.
*/
.comment-form button, .comment-form input[type="submit"] {
    background-color: #007bff; /* 버튼의 배경색을 밝은 파란색(#007bff)으로 설정합니다. */
    color: white; /* 버튼의 글자색을 흰색으로 설정합니다. */
    padding: 10px 20px; /* 상하 10픽셀, 좌우 20픽셀의 내부 여백을 설정합니다. */
    border: none; /* 버튼의 테두리를 제거합니다. */
    border-radius: 5px; /* 테두리 모서리를 5픽셀 둥글게 만듭니다. */
    cursor: pointer; /* 마우스 커서를 포인터 모양으로 변경하여 클릭 가능함을 나타냅니다. */
    font-size: 1em; /* 글꼴 크기를 기본 글꼴 크기와 동일하게 설정합니다. */
    transition: background-color 0.3s ease; /* 배경색 변경 시 0.3초 동안 부드러운 전환 효과를 적용하여 사용자 경험을 향상시킵니다. */
}

/* 댓글 제출 버튼에 마우스 오버 시 (hover) 스타일 */
/*
    이 규칙은 `.comment-form` 내부의 `<button>` 태그와 `input[type="submit"]` 태그에 마우스 커서가 올라갔을 때 적용됩니다.
*/
.comment-form button:hover, .comment-form input[type="submit"]:hover {
    background-color: #0056b3; /* 마우스 오버 시 배경색을 더 진한 파란색(#0056b3)으로 변경합니다. */
}
```

### image_slider.css
```
/*
    이 CSS 코드는 웹 페이지에 동적인 이미지 슬라이더(캐러셀)를 구현하기 위한 스타일을 정의합니다.
    주로 슬라이더의 컨테이너, 실제 이미지가 움직이는 부분, 그리고 이전/다음 버튼과 같은
    컨트롤 요소들의 레이아웃과 시각적 속성을 제어합니다.
*/

/* 슬라이더 전체 컨테이너 스타일 */
/*
    `.slider-image-slider-container`는 이미지 슬라이더 전체를 감싸는 가장 바깥쪽 요소입니다.
    이 컨테이너는 슬라이더의 기본적인 크기, 위치, 그리고 내부 콘텐츠가 넘칠 때의 처리 방식을 정의합니다.
*/
.slider-image-slider-container {
    position: relative; /* 자식 요소인 `.slider-slider-controls`의 `position: absolute;` 기준점이 됩니다. */
    width: 100%; /* 부모 요소의 너비를 100% 차지합니다. */
    max-width: 1000; /* 슬라이더의 최대 너비를 1000픽셀로 제한합니다. (참고: 단위 'px'가 빠져있습니다. '1000px'로 수정하는 것이 좋습니다.) */
    margin-left: auto; /* 좌측 마진을 자동으로 설정하여 컨테이너를 수평 중앙에 배치합니다. */
    margin-right: auto; /* 우측 마진을 자동으로 설정하여 컨테이너를 수평 중앙에 배치합니다. */
    overflow: hidden; /* 컨테이너를 벗어나는 내부 콘텐츠(슬라이드 이미지)를 숨깁니다.
                          이는 여러 이미지가 한 줄에 나열되어 있다가 슬라이딩될 때 중요한 역할을 합니다. */
}

/* 이미지들이 실제 움직이는 슬라이더 부분 스타일 */
/*
    `.slider-image-slider`는 여러 이미지들을 포함하고 있으며, 이 요소 자체가 좌우로 이동하며 슬라이드 효과를 냅니다.
*/
.slider-image-slider {
    display: flex; /* 내부의 이미지들을 가로로 정렬하기 위해 Flexbox 레이아웃을 사용합니다. */
    transition: transform 0.5s ease-in-out; /* `transform` 속성(슬라이더 이동)이 변경될 때
                                                 0.5초 동안 부드럽게 애니메이션되도록 설정합니다.
                                                 'ease-in-out'은 시작과 끝이 느리고 중간이 빠른 전환 효과를 제공합니다. */
}

/* 슬라이더 내부 각 이미지 스타일 */
/*
    `.slider-image-slider img`는 슬라이더 내부에 있는 각각의 이미지 요소에 대한 스타일을 정의합니다.
*/
.slider-image-slider img {
    width: 100%; /* 각 이미지가 부모 요소(`.slider-image-slider`)의 너비를 100% 차지하도록 설정합니다.
                     이때 `.slider-image-slider`는 컨테이너의 너비에 맞게 조정되므로,
                     결과적으로 각 이미지는 컨테이너의 전체 너비를 차지하게 됩니다. */
    height: auto; /* 이미지의 높이를 자동으로 조정하여 원본 이미지의 비율을 유지합니다. */
}

/* 슬라이더 컨트롤 (이전/다음 버튼) 컨테이너 스타일 */
/*
    `.slider-slider-controls`는 이전/다음 버튼을 포함하며, 슬라이더 이미지 위에 오버레이되어 나타납니다.
*/
.slider-slider-controls {
    position: absolute; /* 부모 요소(`.slider-image-slider-container`)를 기준으로 위치를 지정합니다. */
    top: 0; /* 부모 컨테이너의 상단에 정렬합니다. */
    left: 0; /* 부모 컨테이너의 좌측에 정렬합니다. */
    width: 100%; /* 부모 컨테이너의 전체 너비를 차지합니다. */
    height: 100%; /* 부모 컨테이너의 전체 높이를 차지합니다. */
    display: flex; /* 내부 요소(버튼)를 가로로 정렬하고 배치하기 위해 Flexbox 레이아웃을 사용합니다. */
    justify-content: space-between; /* 버튼들을 좌우 양 끝으로 최대한 벌려 배치합니다 (하나는 좌측 끝, 다른 하나는 우측 끝). */
    align-items: center; /* 버튼들을 세로 방향으로 중앙에 정렬합니다. */
    padding: 0 10px; /* 좌우로 10픽셀의 내부 여백을 추가하여 버튼이 컨테이너 가장자리에 너무 붙지 않도록 합니다. */
    box-sizing: border-box; /* 패딩이 요소의 전체 너비와 높이에 포함되도록 계산 방식을 설정합니다.
                                 (패딩 때문에 요소 크기가 예상보다 커지는 것을 방지합니다.) */
}

/* 이전/다음 버튼의 공통 스타일 */
/*
    `.slider-prev-button`과 `.slider-next-button`은 슬라이드를 제어하는 버튼에 대한 공통적인 스타일을 정의합니다.
*/
.slider-prev-button,
.slider-next-button {
    font-size: 24px; /* 버튼 텍스트(예: 화살표 아이콘)의 글꼴 크기를 24픽셀로 설정합니다. */
    padding: 10px; /* 버튼 내부적으로 10픽셀의 여백(패딩)을 추가하여 클릭 영역을 넓힙니다. */
    background: rgba(0, 0, 0, 0.5); /* 배경색을 검정색 반투명(투명도 50%)으로 설정하여 이미지 위에 떠 있는 느낌을 줍니다. */
    color: white; /* 버튼의 글자색을 흰색으로 설정합니다. */
    border: none; /* 버튼의 테두리를 제거합니다. */
    cursor: pointer; /* 마우스 커서를 포인터 모양으로 변경하여 클릭 가능함을 나타냅니다. */
    z-index: 10; /* 다른 요소(예: 슬라이더 이미지) 위에 버튼이 표시되도록 z-index를 높게 설정합니다. */
    transform: translateY(0); /* 초기 상태에서 세로 방향으로 이동 없음(0픽셀)을 명시합니다.
                                   이는 특정 애니메이션 효과(예: 호버 시 이동)를 위한 기준점이 될 수 있습니다. */
}
```

# templates 
### board.html 
- 문의 게시판 목록
```
<!DOCTYPE html>
<html>
<head>
    <title>문의 게시판</title>
    <!-- 
        CSS 파일을 연결합니다. 
        url_for 함수는 Flask에서 정적 파일의 URL을 생성하는 데 사용됩니다.
        'static'은 Flask 애플리케이션의 'static' 폴더를 의미하며, 
        'board.css'는 그 폴더 안에 있는 파일 이름입니다.
    -->
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='board.css') }}">

</head>
<body>
    <div class="board-header">
        <!-- 
            로고 이미지를 클릭하면 홈페이지로 이동하는 링크입니다.
            url_for('index')는 Flask 앱의 'index' 뷰 함수에 해당하는 URL을 생성합니다.
        -->
        <a href="{{ url_for('index') }}" class="logo-link">
            <!-- 
                로고 이미지입니다. 
                alt 속성은 이미지가 로드되지 않았을 때 표시될 텍스트를 제공하여 접근성을 높입니다.
            -->
            <img src="{{ url_for('static', filename='images/logo.png') }}" alt="홈으로" class="logo-img">
        </a>
        <h1>문의 게시판</h1>
        <div class="header-actions">
            <!-- 
                "새 글 작성" 버튼입니다. 
                클릭하면 새 게시물을 작성하는 페이지로 이동합니다.
            -->
            <a href="{{ url_for('new_post') }}" class="action-button">새 글 작성</a>
            <!-- 
                "로그아웃" 버튼입니다. 
                클릭하면 로그아웃 기능을 수행하는 페이지로 이동합니다.
            -->
            <a href="{{ url_for('logout') }}" class="action-button">로그아웃</a>
        </div>
    </div>

    <!-- 
        게시물 목록을 담는 비정렬 목록(unordered list)입니다.
        Jinja2 템플릿 문법을 사용하여 서버에서 전달받은 'posts' 리스트를 반복합니다.
    -->
    <ul class="post-list">
        {% for post in posts %}
        <li class="post-item">
            <div class="post-info">
                <!-- 
                    게시물 제목 링크입니다. 
                    클릭하면 해당 게시물의 상세 페이지로 이동합니다.
                    post.id를 통해 각 게시물의 고유 ID를 URL에 전달합니다.
                -->
                <a href="{{ url_for('view_post', post_id=post.id) }}" class="post-title">{{ post.title }}</a>
                <!-- 
                    게시물 메타 정보(작성자 이름, 작성일)입니다.
                    post.author.username은 게시물 작성자의 사용자 이름을 나타냅니다.
                    post.date_posted는 게시물 작성일시이며, strftime 함수를 사용하여 
                    'YYYY-MM-DD HH:MM' 형식으로 포맷팅합니다.
                -->
                <span class="post-meta">({{ post.author.username }}, {{ post.date_posted.strftime('%Y-%m-%d %H:%M') }})</span>
            </div>
            <!-- 
                현재 로그인한 사용자가 게시물의 작성자와 동일한 경우에만 
                게시물 수정 및 삭제 버튼을 표시합니다.
                'current_user'는 Flask-Login 등에서 제공하는 현재 로그인한 사용자 객체입니다.
            -->
            {% if current_user == post.author %}
            <div class="post-actions">
                <!-- 
                    "수정" 버튼입니다. 
                    클릭하면 해당 게시물을 수정하는 페이지로 이동합니다.
                -->
                <a href="{{ url_for('edit_post', post_id=post.id) }}">수정</a>
                <!-- 
                    "삭제" 버튼입니다. 
                    클릭하면 해당 게시물을 삭제하는 페이지로 이동합니다.
                -->
                <a href="{{ url_for('delete_post', post_id=post.id) }}">삭제</a>
            </div>
            {% endif %}
        </li>
        {% endfor %}
    </ul>
</body>
</html>
```

### bulletin_board.html 
- 일반 게시글 작성 폼
```
<!DOCTYPE html>
<html lang="ko"> <head>
    <!-- 
        CSS 파일을 연결합니다. 
        url_for 함수는 Flask에서 정적 파일의 URL을 생성하는 데 사용됩니다.
        'static'은 Flask 애플리케이션의 'static' 폴더를 의미하며, 
        'bulletin_board.css'는 그 폴더 안에 있는 파일 이름입니다.
        이 link 태그는 보통 head 태그 안에 위치해야 합니다.
    -->
    <link rel="stylesheet" href="{{ url_for('static', filename='bulletin_board.css') }}">

    <!-- 
        문자 인코딩을 UTF-8로 설정합니다. 
        이는 한글을 포함한 다양한 문자를 올바르게 표시하기 위해 필수적입니다.
    -->
    <meta charset="UTF-8">
    <title>게시판</title>
    <!-- 
        또 다른 CSS 파일을 연결합니다. 
        'style.css'는 전반적인 웹사이트 스타일을 담당할 수 있습니다.
        이 link 태그도 head 태그 안에 위치해야 합니다.
    -->
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <!-- 
        페이지의 주요 내용을 담는 컨테이너 div입니다. 
        CSS를 통해 중앙 정렬이나 최대 너비 설정 등 레이아웃을 제어하는 데 사용됩니다.
    -->
    <div class="container">
        <h1>게시판</h1>
        <!-- 
            게시글 목록을 표 형태로 표시하기 위한 table 태그입니다.
            게시글의 제목과 작성일을 구조적으로 보여줍니다.
        -->
        <table>
            <thead>
                <tr> <th>제목</th> <th>작성일</th> </tr>
            </thead>
            <tbody>
                <!-- 
                    Jinja2 템플릿 문법을 사용하여 서버에서 전달받은 'posts' 리스트를 반복합니다.
                    각 'post' 객체는 하나의 게시글을 나타냅니다.
                -->
                {% for post in posts %}
                <tr> <td>
                        <!-- 
                            게시글 제목 링크입니다. 
                            클릭하면 해당 게시글의 상세 페이지로 이동합니다.
                            url_for('view_bulletin_post', post_id=post.id)는 Flask 앱의 
                            'view_bulletin_post' 뷰 함수에 해당하는 URL을 생성하며, 
                            post.id를 통해 각 게시물의 고유 ID를 URL에 전달합니다.
                        -->
                        <a href="{{ url_for('view_bulletin_post', post_id=post.id) }}">{{ post.title }}</a>
                    </td>
                    <td>
                        <!-- 
                            게시글 작성일시입니다.
                            post.date_posted는 게시물 작성일시 객체이며, 
                            strftime 함수를 사용하여 'YYYY-MM-DD HH:MM' 형식으로 포맷팅합니다.
                        -->
                        {{ post.date_posted.strftime('%Y-%m-%d %H:%M') }}
                    </td>
                </tr>
                <!-- 
                    Jinja2의 {% else %} 블록은 'posts' 리스트가 비어 있을 때 실행됩니다.
                    즉, 게시글이 하나도 없을 때 "게시글이 없습니다." 메시지를 표시합니다.
                -->
                {% else %}
                <tr>
                    <!-- 
                        colspan="2"는 이 셀이 두 개의 열(제목, 작성일)을 병합하여 사용함을 의미합니다.
                        게시글이 없을 때 전체 테이블 너비에 걸쳐 메시지를 표시합니다.
                    -->
                    <td colspan="2">게시글이 없습니다.</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        <!-- 
            현재 사용자가 로그인(인증)되어 있을 때만 "새 글 쓰기" 버튼을 표시합니다.
            'current_user.is_authenticated'는 Flask-Login 등에서 제공하는 
            현재 사용자의 인증 상태를 확인하는 속성입니다.
        -->
        {% if current_user.is_authenticated %}
        <!-- 
            "새 글 쓰기" 버튼입니다. 
            클릭하면 새 게시글을 작성하는 페이지로 이동합니다.
            'button' 클래스는 CSS를 통해 버튼 스타일을 적용하는 데 사용됩니다.
        -->
        <a href="{{ url_for('new_bulletin_post') }}" class="button">새 글 쓰기</a>
        {% endif %}
        <!-- 
            "홈으로" 돌아가는 링크입니다. 
            클릭하면 웹사이트의 메인 페이지로 이동합니다.
        -->
        <a href="{{ url_for('index') }}">홈으로</a>
    </div>
</body>
</html>
```

### index.html 
- 메인 페이지
```
<!DOCTYPE html>
<html lang="ko"> <head>
    <!-- 
        문자 인코딩을 UTF-8로 설정합니다. 
        이는 한글을 포함한 다양한 문자를 올바르게 표시하기 위해 필수적입니다.
    -->
    <meta charset="UTF-8">
    <title>회원 관리 및 일반 게시판</title>
    <!-- 
        기본 스타일시트 파일을 연결합니다. 
        url_for 함수는 Flask에서 정적 파일의 URL을 생성하는 데 사용됩니다.
        'static'은 Flask 애플리케이션의 'static' 폴더를 의미하며, 
        'style.css'는 그 폴더 안에 있는 파일 이름입니다.
        이 CSS 파일은 페이지의 전반적인 스타일을 정의합니다.
    -->
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <!-- 
        이미지 슬라이더 관련 스타일시트 파일을 연결합니다. 
        이 CSS 파일은 이미지 슬라이더의 시각적 요소를 정의합니다.
    -->
    <link rel="stylesheet" href="{{ url_for('static', filename='image_slider.css') }}">
</head>

<body>
    <!-- 
        웹사이트의 메인 헤더 섹션입니다. 
        로고와 사용자 인증 관련 링크(로그인/로그아웃, 회원가입)를 포함합니다.
    -->
    <header class="main-header">
        <div class="logo">경성대학교 꿀팁!</div>
        <!-- 
            사용자 인증 관련 네비게이션 섹션입니다. 
            로그인 상태에 따라 다른 링크를 표시합니다.
        -->
        <nav class="user-auth">
            <!-- 
                Jinja2 템플릿 문법을 사용하여 현재 로그인한 사용자(current_user)의 
                인증 상태를 확인합니다.
                'current_user.is_authenticated'는 Flask-Login 등에서 제공하는 
                현재 사용자의 인증 상태를 확인하는 속성입니다.
            -->
            {% if current_user.is_authenticated %}
            <span>
                <!-- 
                    사용자의 프로필 사진이 있을 경우 표시합니다.
                    'current_user.profile_picture'는 사용자 객체에 저장된 프로필 사진 URL입니다.
                -->
                {% if current_user.profile_picture %}
                <img src="{{ current_user.profile_picture }}" alt="프로필 사진" class="profile-pic">
                {% endif %}
                {{ current_user.username }}님 환영합니다!
            </span>
            <!-- 
                로그아웃 링크입니다. 
                클릭하면 로그아웃 기능을 수행하는 페이지로 이동합니다.
                url_for('logout')는 Flask 앱의 'logout' 뷰 함수에 해당하는 URL을 생성합니다.
            -->
            <a href="{{ url_for('logout') }}">로그아웃</a>
            <!-- 
                문의 게시판으로 이동하는 링크입니다.
                url_for('board')는 Flask 앱의 'board' 뷰 함수에 해당하는 URL을 생성합니다.
            -->
            <a href="{{ url_for('board') }}" class="board-link">문의 게시판</a>
            {% else %}
            <!-- 
                사용자가 로그인되어 있지 않을 때 표시되는 링크들입니다.
                로그인 페이지로 이동하는 링크입니다.
            -->
            <a href="{{ url_for('login') }}">로그인</a>
            <a href="{{ url_for('register') }}">회원 가입</a>
            <!-- 
                Google 로그인 페이지로 이동하는 링크입니다. 
                Google OAuth를 통한 로그인을 위한 버튼입니다.
            -->
            <a href="{{ url_for('google_login') }}" class="google-login-btn">Google 로그인</a>
            {% endif %}
        </nav>
    </header>

    <!-- 
        메인 콘텐츠를 감싸는 래퍼입니다. 
        주로 Flexbox나 Grid를 사용하여 좌측, 중앙, 우측 영역을 배치합니다.
    -->
    <div class="main-content-wrapper">
        <!-- 
            좌측 공간입니다. 
            주로 최근 게시글 미리보기를 표시합니다.
        -->
        <div class="left-space board-preview">
            <h2>최근 게시글</h2>
            <ul>
                <!-- 
                    Jinja2 템플릿 문법을 사용하여 서버에서 전달받은 'recent_posts' 리스트를 반복합니다.
                    각 'post' 객체는 하나의 게시글을 나타냅니다.
                -->
                {% for post in recent_posts %}
                <li>
                    <!-- 
                        게시글 제목 링크입니다. 
                        클릭하면 해당 게시글의 상세 페이지로 이동합니다.
                        url_for('view_bulletin_post', post_id=post.id)는 Flask 앱의 
                        'view_bulletin_post' 뷰 함수에 해당하는 URL을 생성하며, 
                        post.id를 통해 각 게시물의 고유 ID를 URL에 전달합니다.
                    -->
                    <a href="{{ url_for('view_bulletin_post', post_id=post.id) }}">{{ post.title }}</a>
                </li>
                <!-- 
                    Jinja2의 {% else %} 블록은 'recent_posts' 리스트가 비어 있을 때 실행됩니다.
                    즉, 최근 게시글이 하나도 없을 때 메시지를 표시합니다.
                -->
                {% else %}
                <li>최근 게시글이 없습니다.</li>
                {% endfor %}
            </ul>
            <!-- 
                "게시판 전체 보기" 링크입니다. 
                클릭하면 일반 게시판 전체 목록 페이지로 이동합니다.
            -->
            <a href="{{ url_for('bulletin_board') }}" class="view-all-board">게시판 전체 보기</a>
        </div>

        <!-- 
            중앙 공간입니다. 
            주로 이미지 슬라이더와 Gemini 검색 섹션을 포함합니다.
        -->
        <div class="middle-space">
            <div class="slider-image-slider-container">
                <!-- 
                    실제 슬라이드되는 이미지들을 담는 컨테이너입니다.
                    JavaScript를 통해 이미지 전환이 제어됩니다.
                -->
                <div class="slider-image-slider">
                    <img src="{{ url_for('static', filename='images/school.png') }}" alt="학교 이미지 1">
                    <img src="{{ url_for('static', filename='images/map.png') }}" alt="학교 지도 실물">
                    <img src="{{ url_for('static', filename='images/lib_in.png') }}" alt="부산 도시 이미지">
                </div>
                <button class="slider-prev-button">&lt;</button>
                <button class="slider-next-button">&gt;</button>
            </div>

            <div class="gemini-search-container">
                <h2>Gemini 검색</h2>
                <!-- 
                    Gemini 검색을 위한 폼입니다. 
                    사용자가 검색어를 입력하고 제출할 수 있습니다.
                -->
                <form id="gemini-form">
                    <input type="text" id="gemini-input" placeholder="Gemini에서 검색하세요">
                    <button type="submit">검색</button>
                </form>
                <div id="gemini-result"></div>
            </div>
        </div>

        <!-- 
            우측 공간입니다. 
            주로 건물 목록을 표시합니다.
        -->
        <div class="right-space">
            <h2>건물 목록</h2>
            <ul class="building-list">
                <li><a href="/building/1">1호관 (한성관)</a></li>
                <li><a href="/building/2">2호관 (자연관)</a></li>
                <li><a href="/building/3">3호관 (예술관)</a></li>
                <li><a href="/building/4">4호관 (상학관)</a></li>
                <li><a href="/building/5">5호관 (사회관)</a></li>
                <li><a href="/building/6">6호관 (인문관)</a></li>
                <li><a href="/building/7">7호관 (제 1공학관)</a></li>
                <li><a href="/building/8">8호관 (제 2공학관)</a></li>
                <li><a href="/building/9">9호관 (약*과학관)</a></li>
                <li><a href="/building/10">10호관 (산학협력관)</a></li>
                <li><a href="/building/11">11호관 (나이팅게일관)</a></li>
                <li><a href="/building/12">12호관 (멀티미디어관)</a></li>
                <li><a href="/building/22">22호관 (문화관)</a></li>
                <li><a href="/building/23">23호관 (제1 학생회관)</a></li>
                <li><a href="/building/24">24호관 (제2 학생회관)</a></li>
                <li><a href="/building/25">25호관 (용무관)</a></li>
                <li><a href="/building/26">26호관 (멀티미디어정보관)</a></li>
                <li><a href="/building/27">27호관 (중앙도서관)</a></li>
                <li><a href="/building/28">28호관 (제1 누리생활관)</a></li>
                <li><a href="/building/29">29호관 (제2 누리생활관)</a></li>
                <li><a href="/building/30">30호관 (건학기념관)</a></li>
            </ul>
        </div>
    </div>

    <!-- 
        메인 섹션입니다. 
        현재는 'display:none;'으로 숨겨져 있지만, 
        향후 동적으로 콘텐츠를 로드하거나 표시할 때 사용될 수 있습니다.
    -->
    <div class="main-section" style="display:none;"></div>

    <!-- 
        이미지 슬라이더 기능을 위한 JavaScript 파일을 연결합니다.
        이 스크립트는 슬라이더의 동작(이미지 전환, 버튼 클릭 이벤트 등)을 제어합니다.
    -->
    <script src="{{ url_for('static', filename='image_slider.js') }}"></script>
    <script>
        // Gemini 검색 폼의 제출 이벤트를 감지하는 이벤트 리스너를 추가합니다.
        document.getElementById('gemini-form').addEventListener('submit', function (event) {
            // 폼의 기본 제출 동작(페이지 새로고침)을 방지합니다.
            event.preventDefault();
            // Gemini 입력 필드에서 사용자가 입력한 검색어를 가져옵니다.
            const query = document.getElementById('gemini-input').value;

            // '/gemini-search' 엔드포인트로 POST 요청을 보냅니다.
            fetch('/gemini-search', {
                method: 'POST', // HTTP 요청 방식은 POST입니다.
                headers: { 
                    'Content-Type': 'application/json' // 요청 본문의 데이터 형식이 JSON임을 명시합니다.
                },
                // 요청 본문에 검색어를 JSON 문자열 형태로 포함합니다.
                body: JSON.stringify({ 'query': query })
            })
            // 서버로부터 응답을 받으면 JSON 형태로 파싱합니다.
            .then(response => response.json())
            // 파싱된 데이터를 사용하여 검색 결과를 화면에 표시합니다.
            .then(data => {
                // 'gemini-result' div에 서버로부터 받은 검색 결과 텍스트를 할당합니다.
                document.getElementById('gemini-result').innerText = data.result;
            })
            // 요청 중 오류가 발생하면 콘솔에 오류를 기록하고 사용자에게 메시지를 표시합니다.
            .catch(error => {
                console.error('Error:', error); // 개발자 콘솔에 오류 메시지를 출력합니다.
                // 'gemini-result' div에 오류 메시지를 표시합니다.
                document.getElementById('gemini-result').innerText = '검색에 실패했습니다.';
            });
        });
    </script>
</body>

</html>
```
### login.html 
- 로그인
```
<!DOCTYPE html>
<html>
<head>
    <title>로그인</title>
    <!-- 
        CSS 파일을 연결합니다. 
        url_for 함수는 Flask에서 정적 파일의 URL을 생성하는 데 사용됩니다.
        'static'은 Flask 애플리케이션의 'static' 폴더를 의미하며, 
        'style.css'는 그 폴더 안에 있는 파일 이름입니다.
        이 CSS 파일은 페이지의 전반적인 스타일을 정의합니다.
    -->
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <h1>로그인</h1>
    <!-- 
        로그인 정보를 제출하기 위한 폼(form)입니다.
        method="POST"는 폼 데이터가 HTTP POST 방식으로 서버로 전송됨을 의미합니다.
        (보안상 민감한 정보인 비밀번호 등을 전송할 때 사용됩니다.)
        action 속성이 명시되지 않았으므로, 현재 페이지의 URL로 데이터가 전송됩니다.
    -->
    <form method="POST">
        <!-- 
            '사용자 이름' 입력 필드에 대한 라벨(label)입니다.
            for="username"은 이 라벨이 id가 'username'인 입력 필드와 연결됨을 나타냅니다.
            사용자가 라벨을 클릭하면 해당 입력 필드로 포커스가 이동합니다.
        -->
        <label for="username">사용자 이름:</label><br> <!-- 
            사용자 이름을 입력받는 텍스트 입력 필드입니다.
            id="username": JavaScript나 CSS에서 이 요소를 참조하기 위한 고유 식별자입니다.
            name="username": 폼 데이터가 서버로 전송될 때 이 필드의 이름으로 사용됩니다.
            required: 이 필드가 비어 있으면 폼 제출을 막고 사용자에게 입력을 요구합니다.
        -->
        <input type="text" id="username" name="username" required><br><br> <!-- 
            '비밀번호' 입력 필드에 대한 라벨입니다.
            for="password"는 이 라벨이 id가 'password'인 입력 필드와 연결됨을 나타냅니다.
        -->
        <label for="password">비밀번호:</label><br> <!-- 
            비밀번호를 입력받는 입력 필드입니다.
            type="password": 입력된 문자가 '*' 또는 '•' 등으로 가려져 표시됩니다.
            id="password": JavaScript나 CSS에서 이 요소를 참조하기 위한 고유 식별자입니다.
            name="password": 폼 데이터가 서버로 전송될 때 이 필드의 이름으로 사용됩니다.
            required: 이 필드가 비어 있으면 폼 제출을 막고 사용자에게 입력을 요구합니다.
        -->
        <input type="password" id="password" name="password" required><br><br> <!-- 
            폼을 제출하는 버튼입니다.
            type="submit": 이 버튼을 클릭하면 폼 데이터가 method 속성에 지정된 방식으로 서버로 전송됩니다.
            value="로그인": 버튼에 표시될 텍스트입니다.
        -->
        <input type="submit" value="로그인">
    </form>
    <!-- 
        회원가입 페이지로 이동하는 링크입니다.
        url_for('register')는 Flask 앱의 'register' 뷰 함수에 해당하는 URL을 생성합니다.
    -->
    <p>아직 계정이 없으신가요? <a href="{{ url_for('register') }}">회원 가입</a></p>
</body>
</html>

```

### new_bulletin_post.html
- 일반 게시글 작성
```
<!DOCTYPE html>
<html lang="ko"> <head>
    <!-- 
        CSS 파일을 연결합니다. 
        url_for 함수는 Flask에서 정적 파일의 URL을 생성하는 데 사용됩니다.
        'static'은 Flask 애플리케이션의 'static' 폴더를 의미하며, 
        'bulletin_board.css'는 그 폴더 안에 있는 파일 이름입니다.
        이 link 태그는 보통 head 태그 안에 위치해야 합니다.
    -->
    <link rel="stylesheet" href="{{ url_for('static', filename='bulletin_board.css') }}">
    
    <!-- 
        문자 인코딩을 UTF-8로 설정합니다. 
        이는 한글을 포함한 다양한 문자를 올바르게 표시하기 위해 필수적입니다.
    -->
    <meta charset="UTF-8">
    <title>새 글 쓰기</title>
    <!-- 
        또 다른 CSS 파일을 연결합니다. 
        'style.css'는 전반적인 웹사이트 스타일을 담당할 수 있습니다.
        이 link 태그도 head 태그 안에 위치해야 합니다.
    -->
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <!-- 
        페이지의 주요 내용을 담는 컨테이너 div입니다. 
        CSS를 통해 중앙 정렬이나 최대 너비 설정 등 레이아웃을 제어하는 데 사용됩니다.
    -->
    <div class="container">
        <h1>새 글 쓰기</h1>
        <!-- 
            새 게시글 작성을 위한 폼(form)입니다.
            method="POST"는 폼 데이터가 HTTP POST 방식으로 서버로 전송됨을 의미합니다.
            action 속성이 명시되지 않았으므로, 현재 페이지의 URL로 데이터가 전송됩니다.
            이 폼은 게시글의 제목과 내용을 입력받습니다.
        -->
        <form method="POST">
            <!-- 
                '제목' 입력 필드에 대한 라벨(label)입니다.
                for="title"은 이 라벨이 name이 'title'인 입력 필드와 연결됨을 나타냅니다.
                (HTML5에서는 label의 for 속성이 input의 id와 일치하는 것이 일반적이지만, name과도 연결될 수 있습니다.)
            -->
            <label for="title">제목:</label>
            <!-- 
                게시글 제목을 입력받는 텍스트 입력 필드입니다.
                name="title": 폼 데이터가 서버로 전송될 때 이 필드의 이름으로 사용됩니다.
                required: 이 필드가 비어 있으면 폼 제출을 막고 사용자에게 입력을 요구합니다.
            -->
            <input type="text" name="title" required><br> <!-- 
                '내용' 입력 필드에 대한 라벨입니다.
                for="content"는 이 라벨이 name이 'content'인 텍스트 영역과 연결됨을 나타냅니다.
            -->
            <label for="content">내용:</label>
            <!-- 
                게시글 내용을 입력받는 여러 줄 텍스트 영역입니다.
                name="content": 폼 데이터가 서버로 전송될 때 이 필드의 이름으로 사용됩니다.
                rows="10": 텍스트 영역의 초기 높이를 10줄로 설정합니다.
                required: 이 필드가 비어 있으면 폼 제출을 막고 사용자에게 입력을 요구합니다.
            -->
            <textarea name="content" rows="10" required></textarea><br> <!-- 
                폼을 제출하는 버튼입니다.
                type="submit": 이 버튼을 클릭하면 폼 데이터가 method 속성에 지정된 방식으로 서버로 전송됩니다.
                value="저장": 버튼에 표시될 텍스트입니다.
            -->
            <input type="submit" value="저장">
        </form>
        <!-- 
            "게시판으로 돌아가기" 링크입니다. 
            클릭하면 일반 게시판 목록 페이지로 이동합니다.
            url_for('bulletin_board')는 Flask 앱의 'bulletin_board' 뷰 함수에 해당하는 URL을 생성합니다.
        -->
        <a href="{{ url_for('bulletin_board') }}">게시판으로 돌아가기</a>
    </div>
</body>
</html>

```
### new_post.html
- 문의 게시글 상세 보기
```
<!DOCTYPE html>
<html lang="ko"> <head>
    <!-- 
        CSS 파일을 연결합니다. 
        url_for 함수는 Flask에서 정적 파일의 URL을 생성하는 데 사용됩니다.
        'static'은 Flask 애플리케이션의 'static' 폴더를 의미하며, 
        'bulletin_board.css'는 그 폴더 안에 있는 파일 이름입니다.
        이 link 태그는 보통 head 태그 안에 위치해야 합니다.
    -->
    <link rel="stylesheet" href="{{ url_for('static', filename='bulletin_board.css') }}">
    
    <!-- 
        문자 인코딩을 UTF-8로 설정합니다. 
        이는 한글을 포함한 다양한 문자를 올바르게 표시하기 위해 필수적입니다.
    -->
    <meta charset="UTF-8">
    <title>새 글 쓰기</title>
    <!-- 
        또 다른 CSS 파일을 연결합니다. 
        'style.css'는 전반적인 웹사이트 스타일을 담당할 수 있습니다.
        이 link 태그도 head 태그 안에 위치해야 합니다.
    -->
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <!-- 
        페이지의 주요 내용을 담는 컨테이너 div입니다. 
        CSS를 통해 중앙 정렬이나 최대 너비 설정 등 레이아웃을 제어하는 데 사용됩니다.
    -->
    <div class="container">
        <h1>새 글 쓰기</h1>
        <!-- 
            새 게시글 작성을 위한 폼(form)입니다.
            method="POST"는 폼 데이터가 HTTP POST 방식으로 서버로 전송됨을 의미합니다.
            action 속성이 명시되지 않았으므로, 현재 페이지의 URL로 데이터가 전송됩니다.
            이 폼은 게시글의 제목과 내용을 입력받습니다.
        -->
        <form method="POST">
            <!-- 
                '제목' 입력 필드에 대한 라벨(label)입니다.
                for="title"은 이 라벨이 name이 'title'인 입력 필드와 연결됨을 나타냅니다.
                (HTML5에서는 label의 for 속성이 input의 id와 일치하는 것이 일반적이지만, name과도 연결될 수 있습니다.)
            -->
            <label for="title">제목:</label>
            <!-- 
                게시글 제목을 입력받는 텍스트 입력 필드입니다.
                name="title": 폼 데이터가 서버로 전송될 때 이 필드의 이름으로 사용됩니다.
                required: 이 필드가 비어 있으면 폼 제출을 막고 사용자에게 입력을 요구합니다.
            -->
            <input type="text" name="title" required><br> <!-- 
                '내용' 입력 필드에 대한 라벨입니다.
                for="content"는 이 라벨이 name이 'content'인 텍스트 영역과 연결됨을 나타냅니다.
            -->
            <label for="content">내용:</label>
            <!-- 
                게시글 내용을 입력받는 여러 줄 텍스트 영역입니다.
                name="content": 폼 데이터가 서버로 전송될 때 이 필드의 이름으로 사용됩니다.
                rows="10": 텍스트 영역의 초기 높이를 10줄로 설정합니다.
                required: 이 필드가 비어 있으면 폼 제출을 막고 사용자에게 입력을 요구합니다.
            -->
            <textarea name="content" rows="10" required></textarea><br> <!-- 
                폼을 제출하는 버튼입니다.
                type="submit": 이 버튼을 클릭하면 폼 데이터가 method 속성에 지정된 방식으로 서버로 전송됩니다.
                value="저장": 버튼에 표시될 텍스트입니다.
            -->
            <input type="submit" value="저장">
        </form>
        <!-- 
            "게시판으로 돌아가기" 링크입니다. 
            클릭하면 일반 게시판 목록 페이지로 이동합니다.
            url_for('bulletin_board')는 Flask 앱의 'bulletin_board' 뷰 함수에 해당하는 URL을 생성합니다.
        -->
        <a href="{{ url_for('bulletin_board') }}">게시판으로 돌아가기</a>
    </div>
</body>
</html>
```
### register.html 
- 회원가입 
```
<!DOCTYPE html>
<html>
<head>
    <title>회원 가입</title>
    <!-- 
        CSS 파일을 연결합니다. 
        url_for 함수는 Flask에서 정적 파일의 URL을 생성하는 데 사용됩니다.
        'static'은 Flask 애플리케이션의 'static' 폴더를 의미하며, 
        'style.css'는 그 폴더 안에 있는 파일 이름입니다.
        이 CSS 파일은 페이지의 전반적인 스타일을 정의합니다.
    -->
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <h1>회원 가입</h1>
    <!-- 
        회원 가입 정보를 제출하기 위한 폼(form)입니다.
        method="POST"는 폼 데이터가 HTTP POST 방식으로 서버로 전송됨을 의미합니다.
        (보안상 민감한 정보인 비밀번호 등을 전송할 때 사용됩니다.)
        action 속성이 명시되지 않았으므로, 현재 페이지의 URL로 데이터가 전송됩니다.
    -->
    <form method="POST">
        <!-- 
            '사용자 이름' 입력 필드에 대한 라벨(label)입니다.
            for="username"은 이 라벨이 id가 'username'인 입력 필드와 연결됨을 나타냅니다.
            사용자가 라벨을 클릭하면 해당 입력 필드로 포커스가 이동합니다.
        -->
        <label for="username">사용자 이름:</label><br> <!-- 
            사용자 이름을 입력받는 텍스트 입력 필드입니다.
            id="username": JavaScript나 CSS에서 이 요소를 참조하기 위한 고유 식별자입니다.
            name="username": 폼 데이터가 서버로 전송될 때 이 필드의 이름으로 사용됩니다.
            required: 이 필드가 비어 있으면 폼 제출을 막고 사용자에게 입력을 요구합니다.
        -->
        <input type="text" id="username" name="username" required><br><br> <!-- 
            '비밀번호' 입력 필드에 대한 라벨입니다.
            for="password"는 이 라벨이 id가 'password'인 입력 필드와 연결됨을 나타냅니다.
        -->
        <label for="password">비밀번호:</label><br> <!-- 
            비밀번호를 입력받는 입력 필드입니다.
            type="password": 입력된 문자가 '*' 또는 '•' 등으로 가려져 표시됩니다.
            id="password": JavaScript나 CSS에서 이 요소를 참조하기 위한 고유 식별자입니다.
            name="password": 폼 데이터가 서버로 전송될 때 이 필드의 이름으로 사용됩니다.
            required: 이 필드가 비어 있으면 폼 제출을 막고 사용자에게 입력을 요구합니다.
        -->
        <input type="password" id="password" name="password" required><br><br> <!-- 
            폼을 제출하는 버튼입니다.
            type="submit": 이 버튼을 클릭하면 폼 데이터가 method 속성에 지정된 방식으로 서버로 전송됩니다.
            value="가입": 버튼에 표시될 텍스트입니다.
        -->
        <input type="submit" value="가입">
    </form>
    <!-- 
        로그인 페이지로 이동하는 링크입니다.
        url_for('login')은 Flask 앱의 'login' 뷰 함수에 해당하는 URL을 생성합니다.
    -->
    <p>이미 계정이 있으신가요? <a href="{{ url_for('login') }}">로그인</a></p>
</body>
</html>
```

### view_bulletin_post.html 
- 일반 게시글 상세 보기 
```
<!DOCTYPE html>
<html lang="ko"> <head>
    <!-- 
        문자 인코딩을 UTF-8로 설정합니다. 
        이는 한글을 포함한 다양한 문자를 올바르게 표시하기 위해 필수적입니다.
    -->
    <meta charset="UTF-8">
    <!-- 
        웹 페이지의 제목을 설정합니다. 
        Jinja2 템플릿 문법을 사용하여 현재 게시글의 제목(post.title)을 동적으로 가져와 표시합니다.
        브라우저 탭에 이 제목이 나타납니다.
    -->
    <title>{{ post.title }}</title>
    <!-- 
        기본 스타일시트 파일을 연결합니다. 
        url_for 함수는 Flask에서 정적 파일의 URL을 생성하는 데 사용됩니다.
        'static'은 Flask 애플리케이션의 'static' 폴더를 의미하며, 
        'style.css'는 그 폴더 안에 있는 파일 이름입니다.
        이 CSS 파일은 페이지의 전반적인 스타일을 정의합니다.
    -->
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <!-- 
        게시판 관련 스타일시트 파일을 연결합니다. 
        이 CSS 파일은 게시글 상세 페이지의 특정 요소들에 대한 스타일을 정의합니다.
    -->
    <link rel="stylesheet" href="{{ url_for('static', filename='bulletin_board.css') }}">
    <!-- 
        댓글 관련 스타일시트 파일을 연결합니다. 
        이 CSS 파일은 댓글 섹션의 시각적 요소를 정의합니다.
    -->
    <link rel="stylesheet" href="{{ url_for('static', filename='comments.css') }}">
</head>

<body>
    <!-- 
        페이지의 주요 내용을 담는 컨테이너 div입니다. 
        CSS를 통해 중앙 정렬이나 최대 너비 설정 등 레이아웃을 제어하는 데 사용됩니다.
    -->
    <div class="container">
        <!-- 
            게시글의 제목을 표시합니다. 
            Jinja2 템플릿 문법을 사용하여 서버에서 전달받은 'post' 객체의 'title' 속성을 가져와 표시합니다.
        -->
        <h1>{{ post.title }}</h1>
        <!-- 
            게시글의 작성일을 표시합니다.
            'post.date_posted'는 게시글 작성일시 객체이며, 
            strftime 함수를 사용하여 'YYYY-MM-DD HH:MM' 형식으로 포맷팅합니다.
        -->
        <p>작성일: {{ post.date_posted.strftime('%Y-%m-%d %H:%M') }}</p>
        <!-- 
            게시글의 내용을 담는 div입니다. 
            'content' 클래스를 통해 CSS 스타일이 적용될 수 있습니다.
            'post.content'는 게시글의 실제 내용을 나타냅니다.
        -->
        <div class="content">
            {{ post.content }}
        </div>
        <!-- 
            "게시판으로 돌아가기" 링크입니다. 
            클릭하면 일반 게시판 목록 페이지로 이동합니다.
            url_for('bulletin_board')는 Flask 앱의 'bulletin_board' 뷰 함수에 해당하는 URL을 생성합니다.
        -->
        <a href="{{ url_for('bulletin_board') }}">게시판으로 돌아가기</a>

        <hr> <!-- 
            댓글 섹션의 전체 컨테이너입니다. 
            'comments-section' 클래스를 통해 CSS 스타일이 적용될 수 있습니다.
        -->
        <div class="comments-section">
            <h2>댓글</h2>
            <!-- 
                Jinja2 템플릿 문법을 사용하여 'post' 객체에 'comments'가 있는지 확인합니다.
                'post.comments'는 해당 게시글에 달린 댓글들의 리스트일 것으로 예상됩니다.
            -->
            {% if post.comments %}
                <ul>
                    <!-- 
                        'post.comments' 리스트를 반복하여 각 댓글을 표시합니다.
                        각 'comment' 객체는 하나의 댓글을 나타냅니다.
                    -->
                    {% for comment in post.comments %}
                    <li>
                        <strong>{{ comment.author.username }}</strong> - 
                        <!-- 
                            댓글 작성일시를 작게 표시합니다.
                            'comment.date_posted'는 댓글 작성일시 객체이며, 
                            strftime 함수를 사용하여 'YYYY-MM-DD HH:MM' 형식으로 포맷팅합니다.
                        -->
                        <small>{{ comment.date_posted.strftime('%Y-%m-%d %H:%M') }}</small><br>
                        {{ comment.content }}
                    </li>
                    {% endfor %}
                </ul>
            {% else %}
                <p>댓글이 없습니다.</p>
            {% endif %}
        </div>

        <hr> <!-- 
            Jinja2 템플릿 문법을 사용하여 현재 로그인한 사용자(current_user)의 
            인증 상태를 확인합니다.
            'current_user.is_authenticated'는 Flask-Login 등에서 제공하는 
            현재 사용자의 인증 상태를 확인하는 속성입니다.
        -->
        {% if current_user.is_authenticated %}
        <!-- 
            댓글 작성을 위한 폼 컨테이너입니다. 
            'comment-form' 클래스를 통해 CSS 스타일이 적용될 수 있습니다.
        -->
        <div class="comment-form">
            <h3>댓글 작성</h3>
            <!-- 
                댓글 작성을 위한 폼(form)입니다.
                action 속성에는 댓글을 추가할 Flask 엔드포인트의 URL이 지정됩니다.
                url_for('add_bulletin_comment', post_id=post.id)는 해당 게시글에 댓글을 추가하는 URL을 생성합니다.
                method="POST"는 폼 데이터가 HTTP POST 방식으로 서버로 전송됨을 의미합니다.
            -->
            <form action="{{ url_for('add_bulletin_comment', post_id=post.id) }}" method="POST">
                <!-- 
                    댓글 내용을 입력받는 여러 줄 텍스트 영역입니다.
                    name="content": 폼 데이터가 서버로 전송될 때 이 필드의 이름으로 사용됩니다.
                    rows="4": 텍스트 영역의 초기 높이를 4줄로 설정합니다.
                    cols="50": 텍스트 영역의 초기 너비를 50글자 너비로 설정합니다.
                    placeholder: 입력 필드가 비어 있을 때 사용자에게 표시될 힌트 텍스트입니다.
                    required: 이 필드가 비어 있으면 폼 제출을 막고 사용자에게 입력을 요구합니다.
                -->
                <textarea name="content" rows="4" cols="50" placeholder="댓글 내용을 입력하세요." required></textarea><br>
                <!-- 
                    댓글 작성을 제출하는 버튼입니다.
                    type="submit": 이 버튼을 클릭하면 폼 데이터가 서버로 전송됩니다.
                -->
                <button type="submit">작성</button>
            </form>
        </div>
        {% else %}
        <!-- 
            사용자가 로그인되어 있지 않을 때 댓글 작성을 위해 로그인하라는 메시지를 표시합니다.
            로그인 페이지로 이동하는 링크를 포함합니다.
        -->
        <p>댓글을 작성하려면 <a href="{{ url_for('login') }}">로그인</a>하세요.</p>
        {% endif %}
    </div>
</body>

</html>

```

### view.html 
- 문의 게시시글 상세보기 
```
<!DOCTYPE html>
<html>
<head>
    <!-- 
        웹 페이지의 제목을 설정합니다. 
        Jinja2 템플릿 문법을 사용하여 서버에서 전달받은 'post' 객체의 'title' 속성을 
        동적으로 가져와 브라우저 탭에 표시합니다.
    -->
    <title>{{ post.title }}</title>
    <!-- 
        댓글 관련 스타일시트 파일을 연결합니다. 
        url_for 함수는 Flask에서 정적 파일의 URL을 생성하는 데 사용됩니다.
        'static'은 Flask 애플리케이션의 'static' 폴더를 의미하며, 
        'comments.css'는 그 폴더 안에 있는 파일 이름입니다.
        이 CSS 파일은 댓글 섹션의 시각적 요소를 정의합니다.
    -->
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='comments.css') }}">
    <!-- 
        게시글 상세 보기 페이지의 전반적인 스타일시트 파일을 연결합니다.
        'view.css'는 이 페이지의 레이아웃, 폰트, 색상 등을 정의합니다.
    -->
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='view.css') }}">
</head>
<body>
    <!-- 
        게시글 상세 보기 페이지의 주요 내용을 담는 컨테이너 div입니다.
        'view-container' 클래스를 통해 CSS 스타일이 적용되어 페이지의 중앙 정렬이나 
        최대 너비 설정 등 레이아웃을 제어합니다.
    -->
    <div class="view-container">
        <!-- 
            게시글의 제목을 표시합니다.
            'post-title' 클래스를 통해 CSS 스타일이 적용되어 제목의 크기, 색상 등을 조절합니다.
            Jinja2 템플릿 문법을 사용하여 'post' 객체의 'title' 속성을 가져와 표시합니다.
        -->
        <h1 class="post-title">{{ post.title }}</h1>
        <!-- 
            게시글의 메타 정보(작성자, 작성일)를 담는 div입니다.
            'post-meta' 클래스를 통해 CSS 스타일이 적용될 수 있습니다.
        -->
        <div class="post-meta">
            <!-- 
                작성자 정보를 표시합니다.
                'meta-line' 클래스를 통해 CSS 스타일이 적용될 수 있습니다.
                'post.author.username'은 게시글 작성자의 사용자 이름을 나타냅니다.
            -->
            <span class="meta-line">작성자: {{ post.author.username }}</span>
            <!-- 
                작성일 정보를 표시합니다.
                'meta-line' 클래스를 통해 CSS 스타일이 적용될 수 있습니다.
                'post.date_posted'는 게시글 작성일시 객체이며, 
                strftime 함수를 사용하여 'YYYY-MM-DD HH:MM:SS' 형식으로 포맷팅합니다.
            -->
            <span class="meta-line">작성일: {{ post.date_posted.strftime('%Y-%m-%d %H:%M:%S') }}</span>
        </div>

        <!-- 
            게시글의 내용을 담는 div입니다.
            'content' 클래스를 통해 CSS 스타일이 적용될 수 있습니다.
            'post.content'는 게시글의 실제 내용을 나타냅니다.
            
            |replace('\n', '<br>') 필터: 게시글 내용에 포함된 줄 바꿈 문자('\n')를 HTML의 <br> 태그로 변환합니다.
                                     이렇게 해야 웹 페이지에서 실제 줄 바꿈으로 렌더링됩니다.
            |safe 필터: HTML 태그가 포함된 문자열을 안전하게(이스케이프하지 않고) 렌더링하도록 지시합니다.
                       이는 사용자가 입력한 내용에 HTML 태그가 있을 경우, 태그가 그대로 적용되도록 합니다.
                       (보안상 XSS 공격에 취약할 수 있으므로, 신뢰할 수 있는 내용에만 사용해야 합니다.)
        -->
        <div class="content">
            {{ post.content|replace('\n', '<br>')|safe }}
        </div>

        <!-- 
            "게시판으로 돌아가기" 링크입니다.
            'back-link' 클래스를 통해 CSS 스타일이 적용될 수 있습니다.
            url_for('board')는 Flask 앱의 'board' 뷰 함수에 해당하는 URL을 생성합니다.
        -->
        <p><a href="{{ url_for('board') }}" class="back-link">← 게시판으로 돌아가기</a></p>

        <!-- 
            Jinja2 템플릿 문법을 사용하여 현재 로그인한 사용자(current_user)가 인증되었고,
            동시에 현재 게시글의 작성자(post.author)와 동일한지 확인합니다.
            이 조건이 참일 경우에만 게시글 수정 및 삭제 버튼을 표시합니다.
        -->
        {% if current_user.is_authenticated and current_user == post.author %}
            <!-- 
                게시글 수정 및 삭제 액션 버튼들을 포함하는 div입니다.
                'post-actions' 클래스를 통해 CSS 스타일이 적용될 수 있습니다.
            -->
            <div class="post-actions">
                <!-- 
                    "수정" 링크입니다.
                    클릭하면 해당 게시글을 수정하는 페이지로 이동합니다.
                    url_for('edit_post', post_id=post.id)는 Flask 앱의 'edit_post' 뷰 함수에 해당하는 URL을 생성하며,
                    post.id를 통해 각 게시물의 고유 ID를 URL에 전달합니다.
                -->
                <a href="{{ url_for('edit_post', post_id=post.id) }}">수정</a> |
                <!-- 
                    "삭제" 링크입니다.
                    클릭하면 해당 게시글을 삭제하는 페이지로 이동합니다.
                    url_for('delete_post', post_id=post.id)는 Flask 앱의 'delete_post' 뷰 함수에 해당하는 URL을 생성하며,
                    post.id를 통해 각 게시물의 고유 ID를 URL에 전달합니다.
                    
                    onclick="return confirm('정말로 삭제하시겠습니까?')" 속성:
                    사용자가 "삭제" 링크를 클릭했을 때 JavaScript의 confirm() 대화 상자를 띄워
                    "정말로 삭제하시겠습니까?"라는 메시지를 표시하고, 사용자의 확인을 받습니다.
                    사용자가 '확인'을 누르면 true를 반환하여 링크 이동이 진행되고, 
                    '취소'를 누르면 false를 반환하여 링크 이동이 취소됩니다.
                -->
                <a href="{{ url_for('delete_post', post_id=post.id) }}" onclick="return confirm('정말로 삭제하시겠습니까?')">삭제</a>
            </div>
        {% endif %}

        <!-- 
            댓글 섹션의 제목입니다.
            'comments-title' 클래스를 통해 CSS 스타일이 적용될 수 있습니다.
        -->
        <h2 class="comments-title">댓글</h2>
        <!-- 
            Jinja2 템플릿 문법을 사용하여 'post' 객체에 'comments'가 있는지 확인합니다.
            'post.comments'는 해당 게시글에 달린 댓글들의 리스트일 것으로 예상됩니다.
        -->
        {% if post.comments %}
            <!-- 
                댓글 목록을 담는 비정렬 목록(unordered list)입니다.
                'comment-list' 클래스를 통해 CSS 스타일이 적용될 수 있습니다.
            -->
            <ul class="comment-list">
                <!-- 
                    'post.comments' 리스트를 반복하여 각 댓글을 표시합니다.
                    각 'comment' 객체는 하나의 댓글을 나타냅니다.
                -->
                {% for comment in post.comments %}
                    <li>
                        <!-- 
                            댓글 작성자의 사용자 이름을 굵게 표시하고, 
                            댓글 작성일시를 괄호 안에 표시합니다.
                            'comment.author.username'은 댓글 작성자의 사용자 이름을 나타냅니다.
                            'comment.date_posted'는 댓글 작성일시 객체이며, 
                            strftime 함수를 사용하여 'YYYY-MM-DD HH:MM:SS' 형식으로 포맷팅합니다.
                        -->
                        <strong>{{ comment.author.username }}</strong> ({{ comment.date_posted.strftime('%Y-%m-%d %H:%M:%S') }}):
                        <!-- 
                            댓글의 내용을 담는 div입니다.
                            'comment-content' 클래스를 통해 CSS 스타일이 적용될 수 있습니다.
                            'comment.content'는 댓글의 실제 내용을 나타냅니다.
                            
                            |replace('\n', '<br>') 필터: 댓글 내용에 포함된 줄 바꿈 문자('\n')를 HTML의 <br> 태그로 변환합니다.
            
                            |safe 필터: HTML 태그가 포함된 문자열을 안전하게(이스케이프하지 않고) 렌더링하도록 지시합니다.
                        -->
                        <div class="comment-content">
                            {{ comment.content|replace('\n', '<br>')|safe }}
                        </div>
                    </li>
                {% endfor %}
            </ul>
        {% else %}
            <!-- 
                댓글이 없을 경우 표시되는 메시지입니다.
                'no-comments-message' 클래스를 통해 CSS 스타일이 적용될 수 있습니다.
            -->
            <p class="no-comments-message">아직 댓글이 없습니다.</p>
        {% endif %}

        <!-- 
            Jinja2 템플릿 문법을 사용하여 현재 로그인한 사용자(current_user)가 인증되었는지 확인합니다.
            인증된 경우에만 댓글 작성 폼을 표시합니다.
        -->
        {% if current_user.is_authenticated %}
            <!-- 
                댓글 작성 폼의 제목입니다.
                'comment-form-title' 클래스를 통해 CSS 스타일이 적용될 수 있습니다.
            -->
            <h3 class="comment-form-title">댓글 작성</h3>
            <!-- 
                댓글 작성을 위한 폼(form)입니다.
                method="POST"는 폼 데이터가 HTTP POST 방식으로 서버로 전송됨을 의미합니다.
                action 속성에는 댓글을 추가할 Flask 엔드포인트의 URL이 지정됩니다.
                url_for('add_comment', post_id=post.id)는 해당 게시글에 댓글을 추가하는 URL을 생성합니다.
                'comment-form' 클래스를 통해 CSS 스타일이 적용될 수 있습니다.
            -->
            <form method="POST" action="{{ url_for('add_comment', post_id=post.id) }}" class="comment-form">
                <!-- 
                    댓글 내용을 입력받는 여러 줄 텍스트 영역입니다.
                    name="content": 폼 데이터가 서버로 전송될 때 이 필드의 이름으로 사용됩니다.
                    rows="5": 텍스트 영역의 초기 높이를 5줄로 설정합니다.
                    required: 이 필드가 비어 있으면 폼 제출을 막고 사용자에게 입력을 요구합니다.
                -->
                <textarea name="content" rows="5" required></textarea><br>
                <!-- 
                    댓글 작성을 제출하는 버튼입니다.
                    type="submit": 이 버튼을 클릭하면 폼 데이터가 서버로 전송됩니다.
                    value="댓글 작성": 버튼에 표시될 텍스트입니다.
                -->
                <input type="submit" value="댓글 작성">
            </form>
        {% else %}
            <!-- 
                사용자가 로그인되어 있지 않을 때 댓글 작성을 위해 로그인하라는 메시지를 표시합니다.
                로그인 페이지로 이동하는 링크를 포함합니다.
            -->
            <p><a href="{{ url_for('login') }}">로그인</a> 후 댓글을 작성할 수 있습니다.</p>
        {% endif %}
    </div>
</body>
</html>
```
### B01.html 
- 1호관 
```
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8" />
    <title>건물 소개 페이지</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='buildingC/B01.css') }}" />
    </head>

<body>
    <header class="page-header">
        <a href="{{ url_for('index') }}" class="logo-link">
            <img src="{{ url_for('static', filename='images/logo.png') }}" alt="홈으로" class="logo-img" />
            </a>
        <h1>1호관 (건물명 1)</h1>
        </header>

    <div class="content-wrapper">
        <div class="left-info">
            <div class="container Fcontainer">
                <div class="top-section">
                    <div class="image-area">
                        <img src="{{ url_for('static', filename='images/buildingI/B1_1.jpg') }}" alt="1호관 이미지" />
                        </div>
                    <div class="summary-area">
                        <ul>
                            <li>위치: 중앙 캠퍼스</li>
                            <li>연면적: 3,000㎡</li>
                            <li>건축 연도: 2001년</li>
                        </ul>
                    </div>
                </div>
                <div class="description-area">
                    <p>테스트1<br>테스트1<br>테스트1<br>테스트1<br>테스트1<br>테스트1<br></p>
                    </div>
            </div>

            <div class="container">
                <div class="top-section">
                    <div class="image-area">
                        <img src="{{ url_for('static', filename='images/buildingI/B1_1.jpg') }}" alt="1호관 이미지" />
                    </div>
                    <div class="summary-area">
                        <ul>
                            <li>위치: 중앙 캠퍼스</li>
                            <li>연면적: 3,000㎡</li>
                            <li>건축 연도: 2001년</li>
                        </ul>
                    </div>
                </div>
                <div class="description-area">
                    <p>1호관은 학교의 주요 행정 시설이 위치해 있으며, 강의실과 연구실로 사용되고 있습니다.</p>
                </div>
            </div>

            </div>

        <aside class="right-list">
            <ul class="building-list">
                <li><a href="/building/1">1호관 (건물명 1)</a></li>
                <li><a href="/building/2">2호관 (건물명 2)</a></li>
                <li><a href="/building/3">3호관 (건물명 3)</a></li>
                <li><a href="/building/4">4호관 (건물명 4)</a></li>
                <li><a href="/building/5">5호관 (건물명 5)</a></li>
                <li><a href="/building/6">6호관 (건물명 6)</a></li>
                <li><a href="/building/7">7호관 (건물명 7)</a></li>
                <li><a href="/building/8">8호관 (건물명 8)</a></li>
                <li><a href="/building/9">9호관 (건물명 9)</a></li>
                <li><a href="/building/10">10호관(건물명 10)</a></li>
                <li><a href="/building/11">11호관 (건물명 11)</a></li>
                <li><a href="/building/12">12호관 (건물명 12)</a></li>
                <li><a href="/building/13">13호관 (건물명 13)</a></li>
                <li><a href="/building/14">14호관 (건물명 14)</a></li>
                <li><a href="/building/15">15호관 (건물명 15)</a></li>
                <li><a href="/building/16">16호관 (건물명 16)</a></li>
                <li><a href="/building/17">17호관 (건물명 17)</a></li>
                <li><a href="/building/18">18호관 (건물명 18)</a></li>
                <li><a href="/building/19">19호관 (건물명 19)</a></li>
                <li><a href="/building/20">20호관 (건물명 20)</a></li>
                <li><a href="/building/21">21호관 (건물명 21)</a></li>
                <li><a href="/building/22">22호관 (건물명 22)</a></li>
                <li><a href="/building/23">23호관 (건물명 23)</a></li>
                <li><a href="/building/24">24호관 (건물명 24)</a></li>
                <li><a href="/building/25">25호관 (건물명 25)</a></li>
                <li><a href="/building/26">26호관 (멀티미디어 정보관)</a></li>
                <li><a href="/building/27">27호관 (중앙도서관)</a></li>
                <li><a href="/building/28">28호관 (건물명 28)</a></li>
                <li><a href="/building/29">29호관 (건물명 29)</a></li>
                <li><a href="/building/30">30호관 (건물명 30)</a></li>
            </ul>
        </aside>
    </div>
</body>

</html>
```

### B26.html 
- 26호관
```
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8" />
    <title>건물 소개 페이지</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='buildingC/B01.css') }}" />
    </head>

<body>
    <header class="page-header">
        <a href="{{ url_for('index') }}" class="logo-link">
            <img src="{{ url_for('static', filename='images/logo.png') }}" alt="홈으로" class="logo-img" />
            </a>
        <h1>26호관 (멀티미디어 정보관)</h1>
        </header>

    <div class="content-wrapper">
        <div class="left-info">
            <div class="container Fcontainer">
                <div class="top-section">
                    <div class="image-area">
                        <img src="{{ url_for('static', filename='images/buildingI/B26_1.jpg') }}" alt="1호관 이미지" />
                        </div>
                    <div class="summary-area">
                        <ul>
                            <li>행정건물</li>
                            <li>학사지원팀</li>
                            <li>소프트웨어 대여</li>
                            <li>조류관</li>
                            <li>미술관</li>
                        </ul>
                    </div>
                </div>
                <div class="description-area">
                    <p>학교의 여러가지 행정을 관리하는 행정건물입니다<br>
                        학사지원팀이 위치해 있으며, 학업 소프트웨어 지원, 조류관등 다양한 시설이 있습니다.<br>
                        건학기념관, 중앙도서관과 함께 학교의 최중요 건물들 중 하나입니다</p>
                    </div>
            </div>

            <div class="container">
                <div class="top-section">
                    <div class="image-area">
                        <img src="{{ url_for('static', filename='images/buildingI/B26_2.jpg') }}" alt="학사지원팀" />
                        </div>
                    <div class="summary-area">
                        <div class="building-name">
                            <h3>학사지원팀</h3>
                            </div>
                        <div class="building-info">
                            <ul>
                                <li>위치: 26호관 2층</li>
                                <li>점심시간 휴게</li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="description-area">
                    <p>경성대 학사지원팀 사무실입니다.<br>
                        대면상담을 통해 비대면지원보다 상세한 도움을 받을 수 있습니다.</p>
                </div>
            </div>

            <div class="container">
                <div class="top-section">
                    <div class="image-area">
                        <img src="{{ url_for('static', filename='images/buildingI/B26_3.jpg') }}" alt="26호관 307호" />
                        </div>
                    <div class="summary-area">
                        <div class="building-name">
                            <h3>네트워크 및 PC서비스실(307호)</h3>
                            </div>
                        <div class="building-info">
                            <ul>
                                <li>위치: 26호관 3층</li>
                                <li>소프트웨어 대여</li>
                                <li>서비스실</li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="description-area">
                    <p>ms 오피스365, 한컴, ADOBI등등 재학생이라면 이곳에서 학업에 필요한 여러 소프트웨어를 대여받을 수 있습니다.<br>.</p>
                    </div>
            </div>

            <div class="container">
                <div class="top-section">
                    <div class="image-area">
                        <img src="{{ url_for('static', filename='images/buildingI/B26_42.jpg') }}" alt="조류관" />
                        </div>
                    <div class="summary-area">
                        <div class="building-name">
                            <h3>조류관</h3>
                        </div>
                        <div class="building-info">
                            <ul>
                                <li>위치: 26호관 지하</li>
                                <li>조류 및 다양한 생물의 모형 전시품</li>
                                <li>자유관람</li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="description-area">
                    <p>수백여종의 새와 동식물의 모형이 전시된 공간입니다.<br>
                        26호관의 지하 전시실에 위치하며 관람시관 동안 제약없이 자유롭게 관람 가능합니다.</p>
                </div>
            </div>


            <div class="container">
                <div class="top-section">
                    <div class="image-area">
                        <img src="{{ url_for('static', filename='images/buildingI/B26_5.jpg') }}" alt="미술관" />
                        </div>
                    <div class="summary-area">
                        <div class="building-name">
                            <h3>미술관</h3>
                        </div>
                        <div class="building-info">
                            <ul>
                                <li>위치: 26호관 지하</li>
                                <li>재학생&졸업생들이 제작한<br>
                                    다양한 종류의 미술작품 전시</li>
                                <li>자유관람</li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="description-area">
                    <p>재학생&졸업생들이 제작한 다양한 종류의 미술작품들이 전시된 공간입니다.<br>
                        26호관의 지하 전시실에 위치하며 관람시관 동안 제약없이 자유롭게 관람 가능합니다.</p>
                </div>
            </div>

            </div>

        <aside class="right-list">
            <ul class="building-list">
                <li><a href="/building/1">1호관 (한성관)</a></li>
                <li><a href="/building/2">2호관 (자연관)</a></li>
                <li><a href="/building/3">3호관 (예술관)</a></li>
                <li><a href="/building/4">4호관 (상학관)</a></li>
                <li><a href="/building/5">5호관 (사회관)</a></li>
                <li><a href="/building/6">6호관 (인문관)</a></li>
                <li><a href="/building/7">7호관 (제 1공학관)</a></li>
                <li><a href="/building/8">8호관 (제 2공학관)</a></li>
                <li><a href="/building/9">9호관 (약*과학관)</a></li>
                <li><a href="/building/10">10호관 (산학협력관)</a></li>
                <li><a href="/building/11">11호관 (나이팅게일관)</a></li>
                <li><a href="/building/12">12호관 (멀티미디어관)</a></li>
                <li><a href="/building/22">22호관 (문화관)</a></li>
                <li><a href="/building/23">23호관 (제1 학생회관)</a></li>
                <li><a href="/building/24">24호관 (제2 학생회관)</a></li>
                <li><a href="/building/25">25호관 (용무관)</a></li>
                <li><a href="/building/26">26호관 (멀티미디어정보관)</a></li>
                <li><a href="/building/27">27호관 (중앙도서관)</a></li>
                <li><a href="/building/28">28호관 (제1 누리생활관)</a></li>
                <li><a href="/building/29">29호관 (제2 누리생활관)</a></li>
                <li><a href="/building/30">30호관 (건학기념관)</a></li>
            </ul>
        </aside>
    </div>
</body>

</html>
```

### B27.html 
- 27호관
```
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8" />
    <title>건물 소개 페이지</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='buildingC/B01.css') }}" />
    </head>

<body>
    <header class="page-header">
        <a href="{{ url_for('index') }}" class="logo-link">
            <img src="{{ url_for('static', filename='images/logo.png') }}" alt="홈으로" class="logo-img" />
            </a>
        <h1>27호관 (중앙도서관)</h1>
        </header>

    <div class="content-wrapper">
        <div class="left-info">
            <div class="container Fcontainer">
                <div class="top-section">
                    <div class="image-area">
                        <img src="{{ url_for('static', filename='images/buildingI/B27_1.jpg') }}" alt="1호관 이미지" />
                        </div>
                    <div class="summary-area">
                        <ul>
                            <li>편의&학과건물</li>
                            <li>도서관</li>
                            <li>체육관</li>
                            <li>이디야커피</li>
                            <li>외부 엘레베이터</li>
                        </ul>
                    </div>
                </div>
                <div class="description-area">
                    <p>여러가지 편의시설이 구비된 건물입니다<br>
                        도서관, 체육관, 이디야커피 등 다양한 편의시설이 준비되어있습니다.<br>
                        평생교육원, 스포츠학과 재학생들이 사용합니다.<br>
                        건학기념관, 중앙도서관과 함께 학교의 최중요 건물들 중 하나입니다</p>
                    </div>
            </div>

            <div class="container">
                <div class="top-section">
                    <div class="image-area">
                        <img src="{{ url_for('static', filename='images/buildingI/B27_2.jpg') }}" alt="중앙도서관 입구" />
                        </div>
                    <div class="summary-area">
                        <div class="building-name">
                            <h3>중앙 도서관</h3>
                            </div>
                        <div class="building-info">
                            <ul>
                                <li>위치: 27호관 5층~8층</li>
                                <li>학색증 지참</li> <li>도서 대여</li>
                                <li>6층 입장</li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="description-area">
                    <p>복층 구조를 가진 경성대학교의 중앙도서관의 메인 시설 입니다.<br>
                        주 출입구는 6층에 위치하며, 입장시 학생증이 필요합니다.</p>
                </div>
            </div>

            <div class="container">
                <div class="top-section">
                    <div class="image-area">
                        <img src="{{ url_for('static', filename='images/buildingI/B27_5.jpg') }}" alt="1호관 이미지" />
                        </div>
                    <div class="summary-area">
                        <div class="building-name">
                            <h3>체육관<h3>
                            </div>
                        <div class="building-info">
                            <ul>
                                <li>위치: 27호관 6층</li>
                                <li>편의시설</li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="description-area">
                    <p>27호관에 부속된 실내 체육관입니다.<br>
                        외부 출입문은 주로 잠겨있기에 6층 메인홀과 연결된 복도의 실내 출입문을 통해서 접근할 수 있습니다.</p>
                </div>
            </div>

            <div class="container">
                <div class="top-section">
                    <div class="image-area">
                        <img src="{{ url_for('static', filename='images/buildingI/B27_3.jpg') }}" alt="이디야커피" />
                        </div>
                    <div class="summary-area">
                        <div class="building-name">
                            <h3>이디야커피<h3>
                            </div>
                        <div class="building-info">
                            <ul>
                                <li>위치: 27호관 6층 메인홀</li>
                                <li>커피숍</li>
                                <li>편의시설</li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="description-area">
                    <p>중앙도서관 6층 메인홀에 위치한 이디야커피 가맹점 입니다.<br>
                        학업에 지친 학생들이 간단한 식음료를 먹으며 휴식을 취할 수 있습니다.</p>
                </div>
            </div>

            <div class="container">
                <div class="top-section">
                    <div class="image-area">
                        <img src="{{ url_for('static', filename='images/buildingI/B27_4.jpg') }}" alt="외부 엘레베이터" />
                        </div>
                    <div class="summary-area">
                        <div class="building-name">
                            <h3>외부 엘레베이터</h3>
                        </div>
                        <div class="building-info">
                            <ul>
                                <li>위치: 경대*부경역 2번 출구 북측 </li>
                                <li>사용 층고: 1~6층</li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="description-area">
                    <p>경성대*부경대역 2번 출구로 나와 북쪽길을 따라가면 볼 수 있습니다.<br>
                        중앙도서관 6층 메인홀과 연결되어 있어 경대 캠퍼스 주출입구의 오르막길을 오르지 않고 캠퍼스의 다른 건물에 접근할 수 있습니다.
                        아침시간엔 사람이 몰리기 때문에 대기줄에 10분가량 소요합니다.</p>
                </div>
            </div>

            </div>

        <aside class="right-list">
            <ul class="building-list">
                <li><a href="/building/1">1호관 (한성관)</a></li>
                <li><a href="/building/2">2호관 (자연관)</a></li>
                <li><a href="/building/3">3호관 (예술관)</a></li>
                <li><a href="/building/4">4호관 (상학관)</a></li>
                <li><a href="/building/5">5호관 (사회관)</a></li>
                <li><a href="/building/6">6호관 (인문관)</a></li>
                <li><a href="/building/7">7호관 (제 1공학관)</a></li>
                <li><a href="/building/8">8호관 (제 2공학관)</a></li>
                <li><a href="/building/9">9호관 (약*과학관)</a></li>
                <li><a href="/building/10">10호관 (산학협력관)</a></li>
                <li><a href="/building/11">11호관 (나이팅게일관)</a></li>
                <li><a href="/building/12">12호관 (멀티미디어관)</a></li>
                <li><a href="/building/22">22호관 (문화관)</a></li>
                <li><a href="/building/23">23호관 (제1 학생회관)</a></li>
                <li><a href="/building/24">24호관 (제2 학생회관)</a></li>
                <li><a href="/building/25">25호관 (용무관)</a></li>
                <li><a href="/building/26">26호관 (멀티미디어정보관)</a></li>
                <li><a href="/building/27">27호관 (중앙도서관)</a></li>
                <li><a href="/building/28">28호관 (제1 누리생활관)</a></li>
                <li><a href="/building/29">29호관 (제2 누리생활관)</a></li>
                <li><a href="/building/30">30호관 (건학기념관)</a></li>
            </ul>
        </aside>
    </div>
</body>

</html>
```

## app.py
```
import os # 운영체제와 상호작용하는 기능을 제공 (예: 환경 변수 접근)
from flask import Flask, render_template, request, redirect, url_for, jsonify, session # Flask 웹 프레임워크의 핵심 모듈 임포트
from flask_sqlalchemy import SQLAlchemy # Flask 애플리케이션에서 SQLAlchemy를 사용하기 위한 확장 기능 임포트
from datetime import datetime # 날짜와 시간을 다루기 위한 모듈 임포트
from werkzeug.security import generate_password_hash, check_password_hash # 비밀번호 해싱 및 검증을 위한 함수 임포트
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user # 사용자 인증 관리를 위한 Flask-Login 확장 기능 임포트
import google.generativeai as genai # Google Gemini API와 상호작용하기 위한 라이브러리 임포트
from authlib.integrations.flask_client import OAuth # OAuth 클라이언트 구현을 위한 Authlib 확장 기능 임포트
from dotenv import load_dotenv # .env 파일에서 환경 변수를 로드하기 위한 라이브러리 임포트

# .env 파일 로드
# 이 함수는 애플리케이션 시작 시 .env 파일에 정의된 환경 변수(예: SECRET_KEY, GOOGLE_CLIENT_ID, API_KEY 등)를
# 시스템 환경 변수로 로드하여 os.getenv() 함수로 접근할 수 있게 합니다.
load_dotenv()

# Flask 애플리케이션 초기화
# __name__은 현재 모듈의 이름을 나타내며, Flask가 리소스(템플릿, 정적 파일)를 찾는 데 사용됩니다.
# template_folder='templates'는 템플릿 파일이 'templates' 디렉토리에 있음을 명시적으로 지정합니다.
app = Flask(__name__, template_folder='templates')

# SQLAlchemy 데이터베이스 URI 설정
# 'sqlite:///database.db'는 프로젝트 루트 디렉토리에 'database.db'라는 SQLite 데이터베이스 파일을 생성합니다.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# SQLAlchemy 이벤트 시스템이 객체 변경 사항을 추적하는 것을 비활성화합니다.
# 이는 메모리 사용량을 줄이고 성능을 향상시킬 수 있지만, 개발 중에는 True로 설정하여 디버깅에 도움을 받을 수도 있습니다.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 애플리케이션의 시크릿 키 설정
# 세션 관리 및 기타 보안 관련 작업에 사용됩니다. .env 파일에서 로드됩니다.
app.secret_key = os.getenv('SECRET_KEY')
# 시크릿 키가 설정되지 않았다면 오류를 발생시켜 개발자가 문제를 인지하도록 합니다.
if not app.secret_key:
    raise ValueError("SECRET_KEY 환경 변수가 설정되지 않았습니다. .env 파일을 확인하세요. (예: python -c \"import os; print(os.urandom(24).hex())\" 로 생성)")

# SQLAlchemy 데이터베이스 객체 초기화
# 이 객체를 통해 데이터베이스 모델을 정의하고 데이터베이스와 상호작용합니다.
db = SQLAlchemy(app)

# Flask-Login LoginManager 초기화
# Flask-Login은 사용자 세션을 관리하고 로그인/로그아웃 기능을 제공합니다.
login_manager = LoginManager()
login_manager.init_app(app) # Flask 앱에 LoginManager를 연결합니다.
login_manager.login_view = 'login' # 로그인되지 않은 사용자가 @login_required 데코레이터가 적용된 페이지에 접근하려 할 때 리다이렉트될 로그인 뷰의 이름을 설정합니다.

# Google OAuth 2.0 설정
# Google Cloud Console에서 발급받은 클라이언트 ID와 시크릿을 환경 변수에서 로드합니다.
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# 디버깅: 클라이언트 ID와 시크릿이 제대로 로드되었는지 확인 (서버 시작 시 터미널에 출력됨)
# 실제 값 대신 부분적으로만 표시하여 보안을 유지합니다.
print(f"DEBUG: Loaded GOOGLE_CLIENT_ID: {'*' * (len(GOOGLE_CLIENT_ID) - 10) + GOOGLE_CLIENT_ID[-10:] if GOOGLE_CLIENT_ID else 'None'}")
print(f"DEBUG: Loaded GOOGLE_CLIENT_SECRET: {'*' * (len(GOOGLE_CLIENT_SECRET) - 5) if GOOGLE_CLIENT_SECRET else 'None'}")

# Google OpenID Connect 구성 정보를 가져올 URL입니다.
# Authlib이 이 URL에서 Google의 인증 엔드포인트, 토큰 엔드포인트 등을 자동으로 발견합니다.
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

# Authlib OAuth 객체 초기화
oauth = OAuth(app)

# Google OAuth 클라이언트 등록
# name: OAuth 공급자의 이름 (여기서는 'google')
# client_id, client_secret: Google Cloud Console에서 발급받은 자격 증명
# server_metadata_url: OpenID Connect 구성 정보를 가져올 URL
# client_kwargs: OAuth 요청에 추가될 매개변수. 'scope'는 사용자로부터 얻을 권한을 지정합니다.
#                'openid'는 OpenID Connect를 사용함을 나타내고, 'email'과 'profile'은 사용자 이메일과 프로필 정보에 대한 접근 권한을 요청합니다.
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url=CONF_URL,
    client_kwargs={'scope': 'openid email profile'},
)

# Gemini API 키 설정 (환경 변수에서 로드)
# API 키는 보안상 코드에 직접 하드코딩하지 않고 환경 변수를 통해 관리하는 것이 좋습니다.
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
# Gemini API 클라이언트 구성. 발급받은 API 키를 설정합니다.
genai.configure(api_key=GENAI_API_KEY)

# Gemini 모델 설정
MODEL_NAME = "gemini-1.5-flash" # 사용할 Gemini 모델의 이름
generation_config = {
    "temperature": 0.9, # 출력의 무작위성(창의성)을 제어합니다. 0에 가까울수록 결정적이고 반복적인 출력을 생성합니다.
    "top_p": 1.0 # 샘플링 시 고려할 토큰의 확률 질량 누적 합계를 제어합니다.
}
safety_settings = [
    # 콘텐츠 필터링 설정: 특정 카테고리의 유해한 콘텐츠 생성을 방지합니다.
    {"category": "harassment", "threshold": "block_medium_and_above"}, # 괴롭힘 관련 콘텐츠 차단
    {"category": "hate_speech", "threshold": "block_medium_and_above"}, # 혐오 발언 관련 콘텐츠 차단
    {"category": "sexually_explicit", "threshold": "block_medium_and_above"} # 성적으로 노골적인 콘텐츠 차단
]
# Gemini 모델 인스턴스 생성
model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    generation_config=generation_config,
    safety_settings=safety_settings
)

# 데이터베이스 모델 정의
# UserMixin을 상속받아 Flask-Login이 필요로 하는 속성(is_authenticated, is_active, is_anonymous, get_id())을 자동으로 제공합니다.
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # 사용자 ID (기본 키, 자동 증가)
    username = db.Column(db.String(80), unique=True, nullable=False) # 사용자 이름 (고유해야 하며, NULL 허용 안 함)
    password = db.Column(db.String(120), nullable=True) # 해싱된 비밀번호 (Google 로그인 사용자는 NULL 허용)
    google_id = db.Column(db.String(120), unique=True, nullable=True) # Google OAuth ID (고유해야 하며, NULL 허용)
    email = db.Column(db.String(120), unique=True, nullable=True) # 이메일 주소 (고유해야 하며, NULL 허용)
    profile_picture = db.Column(db.String(255), nullable=True) # 프로필 사진 URL (NULL 허용)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow) # 가입일 (기본값은 현재 UTC 시간)
    # Post 모델과의 관계 정의: User는 여러 개의 Post를 작성할 수 있습니다.
    # 'Post'는 관계를 맺을 다른 모델의 이름, backref는 Post 모델에서 User 객체에 접근할 때 사용할 이름, lazy는 로딩 전략입니다.
    posts = db.relationship('Post', backref='user_posts', lazy=True)
    # BulletinPost 모델과의 관계 정의: User는 여러 개의 BulletinPost를 작성할 수 있습니다.
    bulletin_posts = db.relationship('BulletinPost', backref='user_bulletin_posts', lazy=True)

    def __repr__(self):
        # 객체를 문자열로 표현할 때 사용됩니다. 디버깅에 유용합니다.
        return f'<User {self.username}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True) # 게시글 ID (기본 키, 자동 증가)
    title = db.Column(db.String(100), nullable=False) # 게시글 제목 (NULL 허용 안 함)
    content = db.Column(db.Text, nullable=False) # 게시글 내용 (TEXT 타입, NULL 허용 안 함)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow) # 작성일 (기본값은 현재 UTC 시간)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # 작성자 User의 ID (외래 키, NULL 허용 안 함)
    # User 모델과의 관계 정의: Post는 한 명의 User에 의해 작성됩니다.
    # 'User'는 관계를 맺을 다른 모델의 이름, backref는 User 모델에서 Post 객체에 접근할 때 사용할 이름, lazy는 로딩 전략입니다.
    author = db.relationship('User', backref='written_posts', lazy=True)
    # Comment 모델과의 관계 정의: Post는 여러 개의 Comment를 가질 수 있습니다.
    # cascade='all, delete-orphan': Post가 삭제될 때 연결된 Comment들도 함께 삭제되도록 합니다.
    comments = db.relationship('Comment', backref='post_comments', cascade='all, delete-orphan', lazy=True)

    def __repr__(self):
        return f'<Post {self.title}>'

class BulletinPost(db.Model):
    id = db.Column(db.Integer, primary_key=True) # 게시글 ID (기본 키, 자동 증가)
    title = db.Column(db.String(100), nullable=False) # 게시글 제목 (NULL 허용 안 함)
    content = db.Column(db.Text, nullable=False) # 게시글 내용 (TEXT 타입, NULL 허용 안 함)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow) # 작성일 (기본값은 현재 UTC 시간)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # 작성자 User의 ID (외래 키, NULL 허용 안 함)
    # User 모델과의 관계 정의: BulletinPost는 한 명의 User에 의해 작성됩니다.
    author = db.relationship('User', backref='written_bulletin_posts', lazy=True)
    # Comment 모델과의 관계 정의: BulletinPost는 여러 개의 Comment를 가질 수 있습니다.
    # cascade='all, delete-orphan': BulletinPost가 삭제될 때 연결된 Comment들도 함께 삭제되도록 합니다.
    comments = db.relationship('Comment', backref='bulletin_post_comments', cascade='all, delete-orphan', lazy=True)

    def __repr__(self):
        return f'<BulletinPost {self.title}>'

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True) # 댓글 ID (기본 키, 자동 증가)
    content = db.Column(db.Text, nullable=False) # 댓글 내용 (TEXT 타입, NULL 허용 안 함)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow) # 작성일 (기본값은 현재 UTC 시간)
    
    # 댓글이 어떤 종류의 게시글에 속하는지 나타내는 외래 키.
    # Post.id 또는 BulletinPost.id 중 하나만 값이 있을 수 있습니다.
    # nullable=True로 설정하여 둘 중 하나는 비어있을 수 있도록 합니다.
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)
    bulletin_post_id = db.Column(db.Integer, db.ForeignKey('bulletin_post.id'), nullable=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # 댓글 작성자 User의 ID (외래 키, NULL 허용 안 함)
    
    # Post 모델과의 관계 정의: Comment는 하나의 Post에 속할 수 있습니다.
    # foreign_keys=[post_id]는 이 관계가 post_id 컬럼을 사용함을 명시합니다.
    # backref='post_comments'는 Post 모델에서 이 댓글에 접근할 때 사용할 이름을 정의합니다.
    post = db.relationship('Post', backref='post_comments', foreign_keys=[post_id], lazy=True)
    # BulletinPost 모델과의 관계 정의: Comment는 하나의 BulletinPost에 속할 수 있습니다.
    # foreign_keys=[bulletin_post_id]는 이 관계가 bulletin_post_id 컬럼을 사용함을 명시합니다.
    # backref='bulletin_comments'는 BulletinPost 모델에서 이 댓글에 접근할 때 사용할 이름을 정의합니다.
    bulletin_post = db.relationship('BulletinPost', backref='bulletin_comments', foreign_keys=[bulletin_post_id], lazy=True)
    
    # User 모델과의 관계 정의: Comment는 한 명의 User에 의해 작성됩니다.
    # backref='authored_comments'는 User 모델에서 이 댓글에 접근할 때 사용할 이름을 정의합니다.
    author = db.relationship('User', backref='authored_comments', lazy=True)

    def __repr__(self):
        return f'<Comment {self.id}>'

# Flask-Login: 사용자 로더 함수
# 세션에서 사용자 ID를 기반으로 User 객체를 로드합니다.
# 이 함수는 Flask-Login이 세션에서 사용자 ID를 가져올 때마다 호출됩니다.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- 라우트 정의 ---

# 루트 URL ('/')에 대한 라우트
@app.route('/')
def index():
    # 최근 게시판 게시글 5개를 작성일 기준으로 내림차순 정렬하여 가져옵니다.
    recent_posts = BulletinPost.query.order_by(BulletinPost.date_posted.desc()).limit(5).all()
    # 'index.html' 템플릿을 렌더링하고, 최근 게시글 목록과 현재 로그인된 사용자 정보를 전달합니다.
    return render_template('index.html', recent_posts=recent_posts, current_user=current_user)

# 회원가입 라우트 ('/register')
@app.route('/register', methods=['GET', 'POST'])
def register():
    # 요청 방식이 POST일 경우 (폼 제출)
    if request.method == 'POST':
        username = request.form['username'] # 폼에서 사용자 이름 가져오기
        password = request.form['password'] # 폼에서 비밀번호 가져오기
        hashed_password = generate_password_hash(password) # 비밀번호를 해싱하여 저장 (보안 강화)
        
        # 이미 존재하는 사용자 이름인지 확인
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "이미 사용 중인 사용자 이름입니다." # 이미 있다면 오류 메시지 반환
        
        # 새로운 사용자 객체 생성 및 데이터베이스에 추가
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit() # 변경사항 커밋
        return redirect(url_for('login')) # 회원가입 성공 후 로그인 페이지로 리다이렉트
    # 요청 방식이 GET일 경우 (페이지 로드)
    return render_template('register.html') # 회원가입 폼 렌더링

# 로그인 라우트 ('/login')
@app.route('/login', methods=['GET', 'POST'])
def login():
    # 요청 방식이 POST일 경우 (폼 제출)
    if request.method == 'POST':
        username = request.form['username'] # 폼에서 사용자 이름 가져오기
        password = request.form['password'] # 폼에서 비밀번호 가져오기
        user = User.query.filter_by(username=username).first() # 데이터베이스에서 사용자 이름으로 사용자 조회
        
        # 사용자가 존재하고 비밀번호가 일치하는지 확인
        if user and check_password_hash(user.password, password):
            login_user(user) # Flask-Login을 사용하여 사용자 로그인 처리 (세션에 사용자 ID 저장)
            return redirect(url_for('index')) # 로그인 성공 후 메인 페이지로 리다이렉트
        else:
            return '로그인 실패: 사용자 이름 또는 비밀번호가 올바르지 않습니다.' # 로그인 실패 메시지 반환
    # 요청 방식이 GET일 경우 (페이지 로드)
    return render_template('login.html') # 로그인 폼 렌더링

# Google 로그인 시작 라우트 ('/login/google')
@app.route('/login/google')
def google_login():
    # Google OAuth 콜백 URL을 생성합니다. _external=True는 절대 URL을 생성하도록 합니다.
    redirect_uri = url_for('google_authorize', _external=True)
    # Authlib을 사용하여 Google OAuth 인증 흐름을 시작합니다.
    # 사용자를 Google 로그인 페이지로 리다이렉트합니다.
    return oauth.google.authorize_redirect(redirect_uri)

# Google OAuth 콜백 처리 라우트 ('/callback')
# Google 로그인 후 Google 서버가 이 URL로 사용자를 리다이렉트합니다.
@app.route('/callback')
def google_authorize():
    try:
        # 디버깅을 위한 출력문
        print(f"\n--- Google OAuth Callback Debug ---")
        print(f"DEBUG: Attempting to authorize access token...")
        # Google로부터 받은 인증 코드를 사용하여 액세스 토큰을 요청하고 파싱합니다.
        # 이 과정에서 Google 서버와 통신합니다.
        token = oauth.google.authorize_access_token()
        print(f"DEBUG: Token acquired: {token}")

        print(f"DEBUG: Attempting to parse ID token...")
        # Authlib 1.0.0 이상에서는 nonce를 parse_id_token()에 명시적으로 전달해야 합니다.
        # nonce는 authorize_redirect() 호출 시 Authlib이 세션에 자동으로 저장합니다.
        user_info = oauth.google.parse_id_token(token, nonce=session.get('nonce'))
        print(f"DEBUG: ID token parsed: {user_info}")

        # 사용자 정보 추출 및 디버깅 출력
        print(f"    - Google ID (sub): {user_info.get('sub')}")
        print(f"    - Email: {user_info.get('email')}")
        print(f"    - Name: {user_info.get('name')}")
        print(f"    - Profile Picture: {user_info.get('picture')}")

        google_id = user_info.get('sub') # Google 고유 사용자 ID
        # 데이터베이스에서 해당 Google ID를 가진 사용자가 있는지 확인
        user = User.query.filter_by(google_id=google_id).first()
        print(f"DEBUG: User lookup by google_id '{google_id}': {'Found' if user else 'Not Found'}")

        if not user:
            # 새로운 Google 로그인 사용자일 경우
            email = user_info.get('email')
            # 이메일을 기반으로 사용자 이름 후보를 생성하거나, 이메일이 없으면 Google ID 기반으로 생성
            username_candidate = email if email else f"google_user_{google_id}"
            
            # 기존 사용자 이름 또는 이메일과 충돌하는지 확인
            existing_user_by_username = User.query.filter_by(username=username_candidate).first()
            existing_user_by_email = User.query.filter_by(email=email).first()

            print(f"DEBUG: New user path: Proposed username: '{username_candidate}'")
            if existing_user_by_username or existing_user_by_email:
                # 충돌 발생 시 사용자 이름 변경 (예: google_ID)
                username = f"google_{google_id}"
                print(f"DEBUG: Conflict detected, modified username to: '{username}')")
                # 만약 이메일이 이미 다른 Google ID와 연결되어 있다면, 이메일 필드를 None으로 설정하여 중복 방지
                if existing_user_by_email and existing_user_by_email.google_id != google_id:
                    email = None
            else:
                username = username_candidate # 충돌 없으면 후보 사용자 이름 사용

            # 새로운 사용자 객체 생성 및 데이터베이스에 추가
            user = User(
                username=username,
                google_id=google_id,
                email=email,
                profile_picture=user_info.get('picture')
            )
            db.session.add(user)
            db.session.commit()
            print(f"DEBUG: New user created in DB: {user}")

        login_user(user) # Flask-Login을 사용하여 사용자 로그인 처리
        print(f"DEBUG: User '{user.username}' (ID: {user.id}) logged in successfully via Google.")
        print(f"--- Google OAuth Callback Debug End ---\n")
        return redirect(url_for('index')) # 로그인 성공 후 메인 페이지로 리다이렉트

    except Exception as e:
        # OAuth 과정 중 오류 발생 시 디버깅 메시지 출력
        print(f"\n!!! CRITICAL ERROR during Google OAuth callback: {e} !!!\n")
        raise e # 오류를 다시 발생시켜 스택 트레이스를 볼 수 있도록 함

# 로그아웃 라우트 ('/logout')
@app.route('/logout')
@login_required # 로그인된 사용자만 접근 가능하도록 합니다.
def logout():
    logout_user() # Flask-Login을 사용하여 사용자 로그아웃 처리 (세션에서 사용자 ID 제거)
    return redirect(url_for('index')) # 로그아웃 후 메인 페이지로 리다이렉트

# 문의 게시판 라우트 ('/board')
@app.route('/board')
@login_required # 로그인된 사용자만 접근 가능하도록 합니다.
def board():
    # 모든 문의 게시글을 작성일 기준으로 내림차순 정렬하여 가져옵니다.
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    # 'board.html' 템플릿을 렌더링하고, 게시글 목록을 전달합니다.
    return render_template('board.html', posts=posts)

# 새 문의 게시글 작성 라우트 ('/post/new')
@app.route('/post/new', methods=['GET', 'POST'])
@login_required # 로그인된 사용자만 접근 가능하도록 합니다.
def new_post():
    # 요청 방식이 POST일 경우 (폼 제출)
    if request.method == 'POST':
        title = request.form['title'] # 폼에서 제목 가져오기
        content = request.form['content'] # 폼에서 내용 가져오기
        # 새로운 Post 객체 생성. author는 현재 로그인된 사용자(current_user)로 자동 설정됩니다.
        post = Post(title=title, content=content, author=current_user)
        db.session.add(post) # 데이터베이스 세션에 추가
        db.session.commit() # 변경사항 커밋
        return redirect(url_for('board')) # 게시글 작성 후 문의 게시판으로 리다이렉트
    # 요청 방식이 GET일 경우 (페이지 로드)
    return render_template('new_post.html') # 새 게시글 작성 폼 렌더링

# 문의 게시글 상세 보기 라우트 ('/post/<int:post_id>')
@app.route('/post/<int:post_id>')
def view_post(post_id):
    # post_id에 해당하는 게시글을 데이터베이스에서 조회합니다.
    # 게시글이 없으면 404 Not Found 오류를 발생시킵니다.
    post = Post.query.get_or_404(post_id)
    # 'view.html' 템플릿을 렌더링하고, 해당 게시글 객체를 전달합니다.
    return render_template('view.html', post=post)

# 문의 게시글 수정 라우트 ('/post/edit/<int:post_id>')
@app.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required # 로그인된 사용자만 접근 가능하도록 합니다.
def edit_post(post_id):
    post = Post.query.get_or_404(post_id) # post_id에 해당하는 게시글 조회
    # 현재 로그인된 사용자가 게시글의 작성자가 아닌 경우 접근 권한 없음 메시지 반환
    if post.author != current_user:
        return '접근 권한이 없습니다.'
    # 요청 방식이 POST일 경우 (폼 제출)
    if request.method == 'POST':
        post.title = request.form['title'] # 폼에서 새 제목 가져와 업데이트
        post.content = request.form['content'] # 폼에서 새 내용 가져와 업데이트
        db.session.commit() # 변경사항 커밋
        return redirect(url_for('view_post', post_id=post.id)) # 수정 후 해당 게시글 상세 페이지로 리다이렉트
    # 요청 방식이 GET일 경우 (페이지 로드)
    return render_template('edit_post.html', post=post) # 수정 폼 렌더링 (기존 내용 채워짐)

# 문의 게시글 삭제 라우트 ('/post/delete/<int:post_id>')
@app.route('/post/delete/<int:post_id>')
@login_required # 로그인된 사용자만 접근 가능하도록 합니다.
def delete_post(post_id):
    post = Post.query.get_or_404(post_id) # post_id에 해당하는 게시글 조회
    # 현재 로그인된 사용자가 게시글의 작성자가 아닌 경우 접근 권한 없음 메시지 반환
    if post.author != current_user:
        return '접근 권한이 없습니다.'
    db.session.delete(post) # 데이터베이스 세션에서 게시글 삭제
    db.session.commit() # 변경사항 커밋
    return redirect(url_for('board')) # 삭제 후 문의 게시판으로 리다이렉트

# 문의 게시글에 댓글 추가 라우트 ('/post/<int:post_id>/comment')
@app.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required # 로그인된 사용자만 댓글 작성 가능하도록 합니다.
def add_comment(post_id):
    post = Post.query.get_or_404(post_id) # post_id에 해당하는 게시글 조회
    content = request.form['content'] # 폼에서 댓글 내용 가져오기
    if content: # 내용이 비어있지 않다면
        # 새로운 Comment 객체 생성. post_id와 author를 설정합니다.
        comment = Comment(content=content, post_id=post.id, author=current_user)
        db.session.add(comment) # 데이터베이스 세션에 추가
        db.session.commit() # 변경사항 커밋
    return redirect(url_for('view_post', post_id=post_id)) # 댓글 작성 후 해당 게시글 상세 페이지로 리다이렉트

# 일반 게시판 라우트 ('/bulletin')
@app.route('/bulletin')
def bulletin_board():
    # 모든 일반 게시글을 작성일 기준으로 내림차순 정렬하여 가져옵니다.
    posts = BulletinPost.query.order_by(BulletinPost.date_posted.desc()).all()
    # 'bulletin_board.html' 템플릿을 렌더링하고, 게시글 목록을 전달합니다.
    return render_template('bulletin_board.html', posts=posts)

# 새 일반 게시글 작성 라우트 ('/bulletin/new')
@app.route('/bulletin/new', methods=['GET', 'POST'])
@login_required # 로그인된 사용자만 접근 가능하도록 합니다.
def new_bulletin_post():
    # 요청 방식이 POST일 경우 (폼 제출)
    if request.method == 'POST':
        title = request.form['title'] # 폼에서 제목 가져오기
        content = request.form['content'] # 폼에서 내용 가져오기
        # 새로운 BulletinPost 객체 생성. author는 현재 로그인된 사용자(current_user)로 자동 설정됩니다.
        post = BulletinPost(title=title, content=content, author=current_user)
        db.session.add(post) # 데이터베이스 세션에 추가
        db.session.commit() # 변경사항 커밋
        return redirect(url_for('bulletin_board')) # 게시글 작성 후 일반 게시판으로 리다이렉트
    # 요청 방식이 GET일 경우 (페이지 로드)
    return render_template('new_bulletin_post.html') # 새 게시글 작성 폼 렌더링

# 일반 게시글 상세 보기 라우트 ('/bulletin/<int:post_id>')
@app.route('/bulletin/<int:post_id>')
def view_bulletin_post(post_id):
    # post_id에 해당하는 게시글을 데이터베이스에서 조회합니다.
    # 게시글이 없으면 404 Not Found 오류를 발생시킵니다.
    post = BulletinPost.query.get_or_404(post_id)
    # 'view_bulletin_post.html' 템플릿을 렌더링하고, 해당 게시글 객체를 전달합니다.
    return render_template('view_bulletin_post.html', post=post)

# 일반 게시글에 댓글 추가 라우트 ('/bulletin/<int:post_id>/comment')
@app.route('/bulletin/<int:post_id>/comment', methods=['POST'])
@login_required # 로그인된 사용자만 댓글 작성 가능하도록 합니다.
def add_bulletin_comment(post_id):
    post = BulletinPost.query.get_or_404(post_id) # post_id에 해당하는 게시글 조회
    content = request.form['content'] # 폼에서 댓글 내용 가져오기
    if content: # 내용이 비어있지 않다면
        # 새로운 Comment 객체 생성. bulletin_post_id와 author를 설정합니다.
        comment = Comment(content=content, bulletin_post_id=post.id, author=current_user)
        db.session.add(comment) # 데이터베이스 세션에 추가
        db.session.commit() # 변경사항 커밋
    return redirect(url_for('view_bulletin_post', post_id=post_id)) # 댓글 작성 후 해당 게시글 상세 페이지로 리다이렉트

# 건물 정보 페이지 라우트 ('/building/<int:id>')
@app.route('/building/<int:id>')
def building_page(id):
    # 건물 ID의 유효성 검사 (예: 1부터 99까지의 ID만 유효)
    if not (1 <= id <= 99):
        return "존재하지 않는 건물입니다.", 404 # 유효하지 않은 ID일 경우 404 오류 반환
    # 건물 ID에 해당하는 템플릿 파일 이름 생성 (예: ID가 1이면 'building/B01.html')
    template_name = f'building/B{id:02d}.html'
    # 해당 템플릿을 렌더링합니다.
    return render_template(template_name)

# Gemini 검색 라우트 ('/gemini-search')
@app.route('/gemini-search', methods=['POST'])
def gemini_search():
    data = request.get_json() # 클라이언트로부터 JSON 형식의 요청 본문 가져오기
    query = data.get('query') # 요청 본문에서 'query' 값 추출
    try:
        # Gemini 모델을 사용하여 쿼리에 대한 콘텐츠를 생성합니다.
        response = model.generate_content(query)
        gemini_results = response.text # 생성된 텍스트 결과 가져오기
    except Exception as e:
        # Gemini API 호출 중 오류 발생 시 오류 메시지 생성
        gemini_results = f"Gemini 검색 오류: {str(e)}"
    # 검색 결과를 JSON 형태로 클라이언트에 반환합니다.
    return jsonify({'result': gemini_results})

# 애플리케이션 컨텍스트 내에서 데이터베이스 테이블 생성
# 이 블록은 애플리케이션이 시작될 때 한 번만 실행되며, 정의된 모든 모델에 따라 데이터베이스 테이블을 생성합니다.
# 이미 테이블이 존재하면 아무것도 하지 않습니다.
with app.app_context():
    db.create_all()

# 애플리케이션 실행
# 이 스크립트가 직접 실행될 때만 Flask 개발 서버를 시작합니다.
# debug=True는 개발 모드를 활성화하여 코드 변경 시 서버가 자동으로 재로드되고, 디버깅 정보가 제공됩니다.
if __name__ == '__main__':
    app.run(debug=True)
```

