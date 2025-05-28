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
├── app.py                     # Flask 애플리케이션의 핵심 로직 (백엔드)
├── .env                       # 환경 변수 (API 키, 시크릿 키 등)
├── templates/                 # HTML 템플릿 파일 (프론트엔드)
│   ├── index.html             # 메인 페이지
│   ├── bulletin_board.html    # 일반 게시판 목록
│   ├── edit_post.html         # 문의 게시글 수정 폼
│   ├── login.html             # 로그인 페이지
│   ├── new_bulletin_post.html # 일반 게시글 작성 폼
│   ├── new_post.html          # 문의 게시글 작성 폼
│   ├── register.html          # 회원가입 페이지
│   ├── view.html              # 문의 게시글 상세 보기
│   ├── view_bulletin_post.html# 일반 게시글 상세 보기
│   ├── building/              # 건물 정보 페이지
│   │   ├── B01.html
│   │   ├── B26.html
│   │   └── B27.html
│   └── board.html             # 문의 게시판 목록
├── static/                    # 정적 파일 (CSS, JavaScript, 이미지)
│   ├── buildingC/             # 건물별 CSS
│   │   └── B01.css
│   ├── images/                # 이미지 파일
│   │   └── ...
│   ├── board.css              # 문의 게시판 스타일
│   ├── bulletin_board.css     # 일반 게시판 스타일
│   ├── comments.css           # 댓글 스타일
│   ├── edit_post.css          # 게시글 수정 폼 스타일
│   ├── image_slider.css       # 이미지 슬라이더 스타일
│   ├── image_slider.js        # 이미지 슬라이더 JavaScript
│   ├── login.css              # 로그인 페이지 스타일
│   ├── new_bulletin_post.css  # 일반 게시글 작성 폼 스타일
│   ├── new_post.css           # 문의 게시글 작성 폼 스타일 
│   ├── register.css           # 회원가입 페이지 스타일 
│   ├── style.css              # 전역 스타일 
│   ├── view.css               # 게시글 상세 보기 스타일 
│   └── view_bulletin_post.css # 일반 게시글 상세 보기 스타일 
└── instance/                  # 데이터베이스 파일
    └── database.db            # SQLite 데이터베이스 파일
```
- `app.py`는 모든 백엔드 로직을 처리하며, `templates` 폴더의 HTML 파일들을 렌더링하여 사용자에게 보여줍니다.
- `static` 폴더는 웹 페이지의 디자인과 동적인 요소를 담당하는 CSS, JavaScript, 이미지 파일들을 포함합니다.
- `instance` 폴더에는 SQLite 데이터베이스 파일이 저장됩니다.
- `.env` 파일은 민감한 API 키와 같은 환경 변수를 안전하게 관리하는 데 사용됩니다.

# 웹 페이지 구성하기

## index.html 
- 메인 페이지
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
- 로그인 페이지 
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
- 회원가입 페이지  
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
- 터미널에서 python을 치면 파이썬 터미널이 열리는 데 이 코드 입력하면 랜덤으로 키를 생성해줌 
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

- .env 파일 
```
# Flask 애플리케이션의 시크릿 키 (세션 관리에 사용)
SECRET_KEY= 
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

# 게시글, 문의 게시글과 건물 추가 등 
## board.html (추가)
- 문의 게시판의 게시글 목록을 보여줌 
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

## bulletin_board.html (추가)
- 일반 게시판의 게시글 목록
```
<!DOCTYPE html>
<html lang="ko"> 
    
<head>
    <meta charset="UTF-8">
    <title>게시판</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='bulletin_board.css') }}">
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

## edit_post.html (추가) 
- 문의 게시글을 수정할 수 있는 폼
```
<!DOCTYPE html>
<html>
<head>
    <title>글 수정</title>
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='edit_post.css') }}">
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

## new_bulletin_post.html (추가)
- 일반 게시판에 새 글을 작성하는 폼
```
<!DOCTYPE html>
<html lang="ko"> 
<head>
    <meta charset="UTF-8">
    <title>새 글 쓰기</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='new_bulletin_post.css') }}">
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

## new_post.html (추가) 
- 문의 게시판에 새 글을 작성하는 폼
```
<!DOCTYPE html>
<html>
<head>
    <title>새 글 작성</title>
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='new_post.css') }}">
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

## view_bulletin_post.html (추가) 
- 일반 게시판 게시글의 상세 내용과 댓글 목록, 그리고 댓글 작성 폼
```
<!DOCTYPE html>
<html lang="ko">

<head>
    <meta charset="UTF-8">
    <title>{{ post.title }}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='view_bulletin_post.css') }}">
</head>

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

## view.html (추가) 
- 문의 게시판 게시글의 상세 내용과 댓글 목록, 그리고 댓글 작성 폼
- 게시글 작성자에게는 수정/삭제 버튼을 보여줌 
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

## board.css (추가)
``` 
/* board.css - 문의 게시판용 밝은 파랑 & 흰색 테마 */

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f0f4f8; /* 밝은 회색 배경 */
    color: #004080; /* 진한 파랑 글자 */
    margin: 0;
    padding: 0 20px;
}

/* 헤더 영역 */
.board-header {
    background-color: #004080;
    color: white;
    display: flex;
    flex-direction: row; /* 기본 가로 정렬 */
    justify-content: space-between; /* 좌우 분리 */
    align-items: center; /* 세로 가운데 정렬 */
    height: 100px; /* 롤백: 고정 높이 */
    padding: 0 20px;
    border-radius: 0 0 8px 8px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);

    margin-bottom: 3px; /* board-header와 post-list 사이 수직 공간 */
}

.logo-link {
    display: flex;
    align-items: center;
    text-decoration: none;
    color: white;
}

.logo-img {
    height: 40px;
    margin-right: 10px;
}

/* h1 문의 게시판 센터 정렬 */
.board-header h1 {
    font-size: 2rem;
    margin: 0 auto; /* 좌우 자동 마진으로 가로 가운데 */
    text-align: center; /* 텍스트 가운데 정렬 */
    flex-grow: 0;
}

/* 오른쪽 버튼들 */
.header-actions {
    display: flex;
    gap: 10px;
}

.action-button {
    background-color: #007bff; /* 약간 밝은 파랑 */
    color: white;
    padding: 8px 16px;
    border-radius: 5px;
    text-decoration: none;
    font-weight: 600;
    box-shadow: 0 2px 4px rgba(0,0,0,0.15);
    transition: background-color 0.3s ease;
}

.action-button:hover {
    background-color: #0056b3;
}

/* 게시글 리스트 */
.post-list {
    list-style: none;
    margin: 0 auto 20px auto; /* 위쪽 0, 좌우 중앙, 아래 20px */
    padding: 20px;
    max-width: 1080px; /* 기존 900px에서 20% 증가 */
    min-height: 60vh; /* 화면 높이의 60% */
    background-color: #e6e9ef; /* 연한 회색 배경 */
    border: 2px solid #004080; /* 진한 파랑 테두리 */
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    overflow-y: auto;
    box-sizing: border-box;
}

.post-item {
    background-color: white;
    border: 1px solid #d0d7e4;
    border-radius: 8px;
    margin-bottom: 15px;
    padding: 15px 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* 게시글 정보 (제목 + 작성자 + 날짜) */
.post-info {
    display: flex;
    flex-direction: column;
}

.post-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #004080;
    text-decoration: none;
    margin-bottom: 5px;
}

.post-title:hover {
    text-decoration: underline;
}

.post-meta {
    font-size: 0.85rem;
    color: #607d8b;
}

/* 게시글 수정/삭제 버튼 */
.post-actions a {
    margin-left: 12px;
    color: #007bff;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.9rem;
    transition: color 0.2s ease;
}

.post-actions a:hover {
    color: #0056b3;
}

/* 반응형: 좁은 화면에서는 버튼을 밑으로 내림 */
@media (max-width: 600px) {
    .board-header {
        flex-direction: column;
        align-items: flex-start;
        height: auto;
        padding: 10px 20px;
        margin-bottom: 10px; /* 모바일에서는 약간 더 공간 줌 */
    }
    .header-actions {
        margin-top: 10px;
        width: 100%;
        justify-content: flex-start;
        gap: 8px;
    }
    .board-header h1 {
        margin: 10px 0;
        text-align: left;
    }
    .post-item {
        flex-direction: column;
        align-items: flex-start;
    }
    .post-actions {
        margin-top: 10px;
        width: 100%;
        display: flex;
        gap: 10px;
    }
}
``` 

## bulletin_board.css (추가) 
``` 
/* 게시판 목록 스타일 */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f0f4f8;
    color: #003060;
    margin: 0;
    padding: 0;
}

.container {
    max-width: 800px;
    margin: 20px auto;
    padding: 20px;
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.container h1 {
    color: #007bff;
    margin-bottom: 20px;
    text-align: center;
}

.container table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
}

.container th, .container td {
    border-bottom: 1px solid #eee;
    padding: 10px;
    text-align: left;
}

.container th {
    background-color: #f8f9fa;
    font-weight: bold;
}

.container tbody tr:hover {
    background-color: #f5f5f5;
}

.container tbody td a {
    text-decoration: none;
    color: #333;
}

.container tbody td a:hover {
    color: #007bff;
    text-decoration: underline;
}

.container .button {
    display: inline-block;
    padding: 10px 15px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    text-decoration: none;
    cursor: pointer;
    margin-right: 10px;
}

.container .button:hover {
    background-color: #0056b3;
}

.container a {
    color: #007bff;
    text-decoration: none;
}

.container a:hover {
    text-decoration: underline;
}
``` 

## comments.css (추가)
``` 
/* comments.css */

/* 댓글 섹션 전체에 대한 스타일 */
.comments-section, h2 + .comment-list, .comment-form { /* view.html의 <h2>댓글</h2> 바로 아래의 ul.comment-list와 .comment-form을 포함 */
    margin-top: 20px;
    padding: 15px;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    background-color: #f9f9f9;
}

/* 댓글 섹션 제목 스타일 */
.comments-section h2, h2.comments-title { /* view.html의 <h2>댓글</h2>에 직접 스타일 적용 */
    font-size: 1.5em;
    color: #333;
    margin-bottom: 15px;
    border-bottom: 2px solid #eee;
    padding-bottom: 10px;
}

/* 댓글 목록 (ul) 스타일 */
.comments-section ul, .comment-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

/* 개별 댓글 (li) 스타일 */
.comments-section ul li, .comment-list li {
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 10px 15px;
    margin-bottom: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.comments-section ul li:last-child, .comment-list li:last-child {
    margin-bottom: 0;
}

/* 댓글 작성자 이름 스타일 */
.comments-section ul li strong, .comment-list li strong {
    color: #007bff;
    font-weight: bold;
}

/* 댓글 작성일자 스타일 */
.comments-section ul li small, .comment-list li small {
    color: #888;
    font-size: 0.85em;
    margin-left: 10px;
}

/* 댓글 내용 스타일 */
.comments-section ul li .comment-content, .comment-list li .comment-content,
.comments-section ul li { /* view_bulletin_post.html의 경우 li 바로 아래 텍스트 */
    line-height: 1.6;
    color: #555;
    white-space: pre-wrap; /* 공백 및 줄바꿈 유지 */
    word-wrap: break-word; /* 긴 단어 줄바꿈 */
}


/* 댓글이 없을 때의 메시지 스타일 */
.comments-section p, p.no-comments-message { /* <p>댓글이 없습니다.</p> 에 적용 */
    color: #777;
    text-align: center;
    padding: 20px;
    background-color: #f0f0f0;
    border-radius: 5px;
}

/* 댓글 작성 폼 (comment-form) 스타일 */
.comment-form {
    margin-top: 30px;
    padding: 20px;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    background-color: #f9f9f9;
}

.comment-form h3 {
    font-size: 1.3em;
    color: #333;
    margin-bottom: 15px;
}

.comment-form textarea {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-sizing: border-box; /* 패딩과 보더가 너비에 포함되도록 */
    margin-bottom: 10px;
    resize: vertical; /* 세로 크기 조절만 허용 */
    min-height: 80px;
}

.comment-form button, .comment-form input[type="submit"] {
    background-color: #007bff;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1em;
    transition: background-color 0.3s ease;
}

.comment-form button:hover, .comment-form input[type="submit"]:hover {
    background-color: #0056b3;
}
``` 

## edit_post.css (추가) 
``` 
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f0f4f8;
    color: #003060;
    padding: 40px;
}

h1 {
    color: #004080;
    text-align: center;
    margin-bottom: 30px;
}

form {
    max-width: 700px;
    margin: 0 auto;
    background-color: #ffffff;
    padding: 25px;
    border: 1px solid #a8c7e7;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
    color: #004080;
}

input[type="text"],
textarea {
    width: 100%;
    padding: 10px;
    margin-bottom: 20px;
    border: 1px solid #a8c7e7;
    border-radius: 4px;
    font-size: 1em;
    box-sizing: border-box;
}

textarea {
    resize: vertical;
}

input[type="submit"] {
    background-color: #004080;
    color: white;
    border: none;
    padding: 10px 20px;
    font-size: 1em;
    border-radius: 4px;
    cursor: pointer;
}

input[type="submit"]:hover {
    background-color: #003060;
}

a {
    display: block;
    text-align: center;
    margin-top: 20px;
    color: #004080;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}
``` 

##  image_slider.css (추가) 
```
.slider-image-slider-container {
    position: relative;
    width: 100%;
    max-width: 1000;
    margin-left: auto;
    margin-right: auto;
    overflow: hidden;
}

.slider-image-slider {
    display: flex;
    transition: transform 0.5s ease-in-out;
}

.slider-image-slider img {
    width: 100%;
    height: auto;
}

.slider-slider-controls {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 10px;
    box-sizing: border-box;
}

.slider-prev-button,
.slider-next-button {
    font-size: 24px;
    padding: 10px;
    background: rgba(0, 0, 0, 0.5);
    color: white;
    border: none;
    cursor: pointer;
    z-index: 10;
    transform: translateY(0);
}
```

## image_slider.js (추가) 

```
document.addEventListener('DOMContentLoaded', function () {
    const sliderContainer = document.querySelector('.slider-image-slider-container');
    const slider = document.querySelector('.slider-image-slider');
    const prevButton = document.querySelector('.slider-prev-button');
    const nextButton = document.querySelector('.slider-next-button');
    const images = slider.querySelectorAll('img');
    const imageCount = images.length;
    let currentIndex = 0;
    let intervalId;
    const autoSlideInterval = 10000;

    // 이미지 슬라이더 너비 동적 조절
    slider.style.width = (imageCount * 100) + '%';
    images.forEach(img => {
        img.style.width = (100 / imageCount) + '%';
    });

    function updateSlider() {
        const translateX = -currentIndex * (100 / imageCount) + '%';
        slider.style.transform = 'translateX(' + translateX + ')';
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % imageCount;
        updateSlider();
    }

    function prevSlide() {
        currentIndex = (currentIndex - 1 + imageCount) % imageCount;
        updateSlider();
    }

    function startAutoSlide() {
        intervalId = setInterval(nextSlide, autoSlideInterval);
    }

    function stopAutoSlide() {
        clearInterval(intervalId);
    }

    if (prevButton && nextButton) {
        prevButton.addEventListener('click', () => {
            stopAutoSlide();
            prevSlide();
            startAutoSlide();
        });

        nextButton.addEventListener('click', () => {
            stopAutoSlide();
            nextSlide();
            startAutoSlide();
        });
    }

    if (sliderContainer) {
        sliderContainer.addEventListener('mouseenter', stopAutoSlide);
        sliderContainer.addEventListener('mouseleave', startAutoSlide);
    }

    startAutoSlide();
});
```

## login.css (추가) 
```
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f0f4f8;
    color: #003060;
    line-height: 1.6;
}

form {
    max-width: 400px;
    margin: 20px auto;
    padding: 20px;
    background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h1 {
    text-align: center;
    color: #004080;
    margin-bottom: 20px;
}

label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
    color: #003060;
}

input[type="text"],
input[type="password"] {
    width: calc(100% - 20px);
    padding: 10px;
    margin-bottom: 15px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 16px;
}

input[type="submit"] {
    background-color: #007bff;
    color: white;
    padding: 12px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 18px;
    width: 100%;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    transition: background-color 0.3s ease;
}

input[type="submit"]:hover {
    background-color: #0056b3;
}

p {
    text-align: center;
    margin-top: 20px;
}

p a {
    color: #007bff;
    text-decoration: none;
    font-weight: bold;
}

p a:hover {
    text-decoration: underline;
}
```

## new_bulletin_post.css (추가) 
```
/* 컨테이너 스타일 */
.container {
    max-width: 800px;
    margin: 20px auto;
    padding: 20px;
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

/* 제목 스타일 */
.container h1 {
    color: #007bff;
    margin-bottom: 20px;
    text-align: center;
}

/* 폼 라벨 */
.container form label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
    color: #555;
}

/* 텍스트 입력창 및 텍스트에어리어 */
.container form input[type="text"],
.container form textarea {
    width: 100%;
    padding: 10px;
    margin-bottom: 15px;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
    font-size: 1em;
}

/* 텍스트에어리어 조절 */
.container form textarea {
    resize: vertical;
    min-height: 150px;
}

/* 저장 버튼 */
.container form input[type="submit"] {
    background-color: #28a745;
    color: white;
    padding: 10px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1em;
}

.container form input[type="submit"]:hover {
    background-color: #218838;
}

/* 링크 스타일 */
.container a {
    color: #007bff;
    text-decoration: none;
}

.container a:hover {
    text-decoration: underline;
}
```

## new_post.css (추가) 
```
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f0f4f8;
    color: #003060;
    line-height: 1.6;
}

form {
    max-width: 700px;
    margin: 20px auto;
    padding: 20px;
    background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h1 {
    text-align: center;
    color: #004080;
    margin-bottom: 20px;
}

label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
    color: #003060;
}

input[type="text"],
textarea {
    width: calc(100% - 20px);
    padding: 10px;
    margin-bottom: 15px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 16px;
}

textarea {
    resize: vertical;
}

input[type="submit"] {
    background-color: #007bff;
    color: white;
    padding: 12px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 18px;
    width: 100%;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    transition: background-color 0.3s ease;
}

input[type="submit"]:hover {
    background-color: #0056b3;
}

p {
    text-align: center;
    margin-top: 20px;
}

p a {
    color: #007bff;
    text-decoration: none;
    font-weight: bold;
}

p a:hover {
    text-decoration: underline;
}
```

## register.css (추가) 
```
/* register.html용 스타일 */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f0f4f8;
    color: #003060;
    line-height: 1.6;
}

form {
    max-width: 400px;
    margin: 20px auto;
    padding: 20px;
    background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h1 {
    text-align: center;
    color: #004080;
    margin-bottom: 20px;
}

label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
    color: #003060;
}

input[type="text"],
input[type="password"] {
    width: calc(100% - 20px);
    padding: 10px;
    margin-bottom: 15px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 16px;
}

input[type="submit"] {
    background-color: #007bff;
    color: white;
    padding: 12px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 18px;
    width: 100%;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    transition: background-color 0.3s ease;
}

input[type="submit"]:hover {
    background-color: #0056b3;
}

p {
    text-align: center;
    margin-top: 20px;
}

p a {
    color: #007bff;
    text-decoration: none;
    font-weight: bold;
}

p a:hover {
    text-decoration: underline;
}
```

## view.css (추가) 
```
body {
    font-family: sans-serif;
    margin: 30px;
    background-color: #f9f9f9;
    color: #333;
}

.view-container {
    max-width: 800px;
    margin: auto;
    background: white;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.post-title {
    text-align: center;
    color: #007bff;
    margin-bottom: 10px;
}

.post-meta {
    text-align: right;
    font-size: 0.9em;
    color: #666;
    margin-bottom: 20px;
}

.meta-line {
    display: block;
}

.content {
    min-height: 150px;
    background-color: #fff;
    border: 1px solid #cccccc71;
    padding: 15px;
    margin: 20px 0;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    line-height: 1.6;
}

.back-link {
    color: #007bff;
    text-decoration: none;
}

.back-link:hover {
    text-decoration: underline;
}

.post-actions {
    text-align: right;
    margin-bottom: 20px;
}

.comment-list {
    list-style: none;
    padding: 0;
}

.comment-list li {
    padding: 10px 0;
    border-top: 1px solid #ccc;     /* 상단 구분선 추가 */
    border-bottom: 1px solid #ccc;  /* 기존 하단 구분선 유지 또는 색상 통일 */
}

.comment-list strong {
    font-weight: bold;
}

.comment-content {
    padding: 0 !important;
    margin: 0 !important;
    text-align: left !important;
}

.comment-form textarea {
    width: 100%;
    padding: 10px;
    box-sizing: border-box;
    margin-bottom: 10px;
}

.comment-form input[type="submit"] {
    background-color: #007bff;
    color: white;
    padding: 8px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.comment-form input[type="submit"]:hover {
    background-color: #0056b3;
}
```
## view_bulletin_post.css (추가) 
```
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f0f4f8;
    color: #003060;
    margin: 0;
    padding: 0;
}

.container {
    max-width: 1100px;
    margin: 20px auto;
    padding: 20px;
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.container h1 {
    color: #007bff;
    margin-bottom: 20px;
    text-align: center;
}

.container a {
    color: #007bff;
    text-decoration: none;
}

.container a:hover {
    text-decoration: underline;
}

.content {
    min-width: 320px;           /* 최소 가로 너비 */
    min-height: 280px;          /* 최소 세로 높이 */
    padding: 20px;              /* 내부 여백 */
    background-color: #ffffff;  /* 흰색 배경 */
    border: 1px solid #ddd;     /* 연한 회색 테두리 */
    border-radius: 5px;         /* 모서리 둥글게 */
    box-shadow: 0 2px 5px rgba(0,0,0,0.1); /* 약한 그림자 */
    margin: 20px 0;             /* 위아래 마진 */
}


/* 댓글 섹션 */
.comments-section {
    margin-top: 20px;
    padding: 15px;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    background-color: #f9f9f9;
}

.comments-section h2 {
    font-size: 1.5em;
    color: #333;
    margin-bottom: 15px;
    border-bottom: 2px solid #eee;
    padding-bottom: 10px;
}

.comments-section ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.comments-section ul li {
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 2px 4px;        /* 기존 10px에서 8px로 줄임 */
    margin-bottom: 8px;       /* 기존 10px에서 8px로 줄임 */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    line-height: 1.6;
    color: #555;
    white-space: pre-wrap;
    word-wrap: break-word;
}

.comments-section ul li strong {
    color: #007bff;
    font-weight: bold;
}

.comments-section ul li small {
    color: #888;
    font-size: 0.85em;
    margin-left: 10px;
}

.comments-section p {
    color: #777;
    text-align: center;
    padding: 20px;
    background-color: #f0f0f0;
    border-radius: 5px;
}

/* 댓글 작성 폼 */
.comment-form {
    margin-top: 30px;
    padding: 20px;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    background-color: #f9f9f9;
}

.comment-form h3 {
    font-size: 1.3em;
    color: #333;
    margin-bottom: 15px;
}

.comment-form textarea {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-sizing: border-box;
    margin-bottom: 10px;
    resize: vertical;
    min-height: 80px;
}

.comment-form button {
    background-color: #007bff;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1em;
    transition: background-color 0.3s ease;
}

.comment-form button:hover {
    background-color: #0056b3;
}
```

## index.html (수정)   
```
<!DOCTYPE html>
<html lang="ko">

<head>
    <meta charset="UTF-8">
    <title>회원 관리 및 일반 게시판</title> 
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='image_slider.css') }}">
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
            <a href="{{ url_for('board') }}" class="board-link">문의 게시판</a>
            {% else %}
            <a href="{{ url_for('login') }}">로그인</a>
            <a href="{{ url_for('register') }}">회원 가입</a>
            {% endif %}
        </nav>
    </header>

    <div class="main-content-wrapper">
        <div class="left-space board-preview">
            <h2>최근 게시글</h2>
            <ul>
                {% for post in recent_posts %}
                <li><a href="{{ url_for('view_bulletin_post', post_id=post.id) }}">{{ post.title }}</a></li>
                {% else %}
                <li>최근 게시글이 없습니다.</li>
                {% endfor %}
            </ul>
            <a href="{{ url_for('bulletin_board') }}" class="view-all-board">게시판 전체 보기</a>
        </div>

        <div class="middle-space">
            <div class="slider-image-slider-container">
                <div class="slider-image-slider">
                    <img src="{{ url_for('static', filename='images/school.png') }}" alt="학교 지도 그림">
                    <img src="{{ url_for('static', filename='images/map.png') }}" alt="학교 지도 실물">
                    <img src="{{ url_for('static', filename='images/lib_in.png') }}" alt="도서관 이미지">
                </div>
                <button class="slider-prev-button">&lt;</button>
                <button class="slider-next-button">&gt;</button>
            </div>
        </div>
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
    <div class="main-section" style="display:none;"></div>

    <script src="{{ url_for('static', filename='image_slider.js') }}"></script>
</body>

</html>
```

## login.html (수정)
```
<!DOCTYPE html>
<html>
<head>
    <title>로그인</title>
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='login.css') }}">
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

## register.html (수정) 
```
<!DOCTYPE html>
<html>
<head>
    <title>회원 가입</title>
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='register.css') }}">
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

## app.py (수정)  
```
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
from datetime import datetime # datetime 모듈을 임포트합니다.

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

app = Flask(__name__, template_folder='templates')
# os.getenv()를 사용하여 환경 변수에서 SECRET_KEY를 가져옵니다.
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'default_fallback_key' # SECRET_KEY 환경 변수가 없으면 'default_fallback_key'를 사용 (개발용)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# .env 파일에서 시크릿 키를 로드합니다.
app.secret_key = os.getenv('SECRET_KEY')
if not app.secret_key:
    raise ValueError("SECRET_KEY 환경 변수가 설정되지 않았습니다. .env 파일을 확인하세요. (예: python -c \"import os; print(os.urandom(24).hex())\" 로 생성)")

# SQLAlchemy 인스턴스 초기화
db = SQLAlchemy(app)

# Flask-Login 설정
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 데이터베이스 모델 정의
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=True)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='user_posts', lazy=True)
    bulletin_posts = db.relationship('BulletinPost', backref='user_bulletin_posts', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref='written_posts', lazy=True)
    comments = db.relationship('Comment', backref='post_comments', cascade='all, delete-orphan', lazy=True)

    def __repr__(self):
        return f'<Post {self.title}>'

class BulletinPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref='written_bulletin_posts', lazy=True)
    comments = db.relationship('Comment', backref='bulletin_post_comments', cascade='all, delete-orphan', lazy=True)

    def __repr__(self):
        return f'<BulletinPost {self.title}>'

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)
    bulletin_post_id = db.Column(db.Integer, db.ForeignKey('bulletin_post.id'), nullable=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    post = db.relationship('Post', backref='post_comments', foreign_keys=[post_id], lazy=True)
    bulletin_post = db.relationship('BulletinPost', backref='bulletin_comments', foreign_keys=[bulletin_post_id], lazy=True)
    
    author = db.relationship('User', backref='authored_comments', lazy=True)

    def __repr__(self):
        return f'<Comment {self.id}>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    recent_posts = BulletinPost.query.order_by(BulletinPost.date_posted.desc()).limit(5).all()
    return render_template('index.html', recent_posts=recent_posts, current_user=current_user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "이미 사용 중인 사용자 이름입니다."
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return '로그인 실패: 사용자 이름 또는 비밀번호가 올바르지 않습니다.'
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/board')
@login_required
def board():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('board.html', posts=posts)

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post = Post(title=title, content=content, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('board'))
    return render_template('new_post.html')

@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('view.html', post=post)

@app.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        return '접근 권한이 없습니다.'
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('view_post', post_id=post.id))
    return render_template('edit_post.html', post=post)

@app.route('/post/delete/<int:post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        return '접근 권한이 없습니다.'
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('board'))

@app.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    content = request.form['content']
    if content:
        # 일반 게시글의 댓글은 post_id만 채웁니다.
        comment = Comment(content=content, post_id=post.id, author=current_user)
        db.session.add(comment)
        db.session.commit()
    return redirect(url_for('view_post', post_id=post_id))

@app.route('/bulletin')
def bulletin_board():
    posts = BulletinPost.query.order_by(BulletinPost.date_posted.desc()).all()
    return render_template('bulletin_board.html', posts=posts)

@app.route('/bulletin/new', methods=['GET', 'POST'])
@login_required
def new_bulletin_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post = BulletinPost(title=title, content=content, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('bulletin_board'))
    return render_template('new_bulletin_post.html')

@app.route('/bulletin/<int:post_id>')
def view_bulletin_post(post_id):
    post = BulletinPost.query.get_or_404(post_id)
    return render_template('view_bulletin_post.html', post=post)

@app.route('/bulletin/<int:post_id>/comment', methods=['POST'])
@login_required
def add_bulletin_comment(post_id):
    post = BulletinPost.query.get_or_404(post_id)
    content = request.form['content']
    if content:
        # 게시판 게시글의 댓글은 bulletin_post_id만 채웁니다.
        comment = Comment(content=content, bulletin_post_id=post.id, author=current_user)
        db.session.add(comment)
        db.session.commit()
    return redirect(url_for('view_bulletin_post', post_id=post_id))

@app.route('/building/<int:id>')
def building_page(id):
    if not (1 <= id <= 99):
        return "존재하지 않는 건물입니다.", 404
    template_name = f'building/B{id:02d}.html'
    return render_template(template_name)


# 애플리케이션 컨텍스트 내에서 데이터베이스 테이블 생성
with app.app_context():
    db.create_all()


# 애플리케이션 실행
if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=8000, debug=True)  # 호스트와 포트를 지정하여 실행할 경우
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

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f0f4f8;
    color: #003060;
    line-height: 1.6;
}

a {
    color: #004080;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

/* 헤더 스타일 */
.main-header {
    background-color: #004080;
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

.user-auth {
    display: flex;
    align-items: center;
}

.user-auth a {
    margin-left: 20px;
    padding: 5px 10px;
    border-radius: 5px;
    text-decoration: none;
    border: 1px solid #004080;
    background-color: white;
    color: #004080;
}

.user-auth a:hover {
    background-color: #004080;
    color: white;
}

.user-auth a.board-link {
    background-color: #66aaff;
    border-color: #66aaff;
    color: white;
}

.user-auth a.board-link:hover {
    background-color: #4c90e0;
} 
.profile-pic {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    vertical-align: middle;
    margin-right: 8px;
    border: 1px solid #eee;
}

/* 메인 콘텐츠 영역 */
.main-content-wrapper {
    display: flex;
    align-items: flex-start;
    width: 100%;
    max-width: 2000px;
    margin: 20px auto;
    gap: 20px;
}

.left-space {
    flex: 0 0 25%;
    padding: 20px;
    background-color: #ffffff;
    border: 1px solid #a8c7e7;
    border-radius: 5px;
    max-width: 500px;
}

.middle-space {
    flex: 1 1 auto;
    max-width: 1050px;
    background-color: #ffffff;
    border: 1px solid #a8c7e7;
    border-radius: 5px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
}

.image-slider-container {
    position: relative;
    overflow: hidden;
    border-radius: 4px;
    width: 100%;
    max-width: 1000px;
}

.image-slider {
    display: flex;
    transition: transform 0.5s ease-in-out;
    width: 100%;
}

.image-slider img {
    width: 100%;
    flex-shrink: 0;
    height: 300px;
    object-fit: cover;
    display: block;
}

.right-space {
    flex: 0 0 25%;
    padding: 40px;
    background-color: #ffffff;
    border: 1px solid #a8c7e7;
    border-radius: 5px;
    max-width: 200px;
}

.building-list h2 {
    color: #004080;
    border-bottom: 2px solid #a8c7e7;
    padding-bottom: 5px;
    margin-bottom: 10px;
}

.building-list ul {
    list-style: none;
    padding-left: 0;
}

.building-list li {
    padding: 5px 0;
    border-bottom: 1px solid #d0dbe8;
}

.building-list li a {
    color: #004080;
    font-weight: 600;
}

/* 슬라이더 네비게이션 버튼 */
.prev-button,
.next-button {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background-color: rgba(0, 64, 128, 0.6);
    border: none;
    color: white;
    font-size: 1.5em;
    padding: 5px 10px;
    cursor: pointer;
    border-radius: 3px;
    user-select: none;
}

.prev-button {
    left: 10px;
}

.next-button {
    right: 10px;
}
```

## 건물 구현 
### B01.html 
- templates 폴더에 building 폴더를 만들고 안에 넣기
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
        <!-- 좌측 정보 영역: 여러 개 복제 가능하도록 div.container -->
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
                    <p>정말<br>아주<br>멋진<br>1호관<br>건물<br>입니다<br></p>
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

            <!-- 필요하면 container 복제해서 더 추가 가능 -->

        </div>

        <!-- 우측 건물 목록 -->
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
- templates 폴더에 building 폴더를 만들고 안에 넣기 
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
        <!-- 좌측 정보 영역: 여러 개 복제 가능하도록 div.container -->
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

            <!-- 필요하면 container 복제해서 더 추가 가능 -->

        </div>

        <!-- 우측 건물 목록 -->
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
- templates 폴더에 building 폴더를 만들고 안에 넣기
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
        <!-- 좌측 정보 영역: 여러 개 복제 가능하도록 div.container -->
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
                    <p>여러가짖 편의시설이 구비된 건물입니다<br>
                        도서관, 체육관, 이디야커피등 다양한 편의시설의 준비되어있습니다.<br>
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
                                <li>학색증 지참</li>
                                <li>도서 대여</li>
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
                    <p>중앙도서관 6층 메인홀에 위치한 이디아커피 가맹점 입니다.<br>
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

            <!-- 필요하면 container 복제해서 더 추가 가능 -->

        </div>

        <!-- 우측 건물 목록 -->
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

### B01.css (추가) 
- static 폴더에 buildingC 폴더를 만들어서 넣기
```
/* 전체 페이지 기본 설정 */
body {
    margin: 0;
    font-family: Arial, sans-serif;
    background-color: #f9f9f9;
}

/* 헤더 스타일 */
.page-header {
    background-color: #004080;
    color: white;
    padding: 20px;
    text-align: center;
}

/* content-wrapper: 좌우 영역 배치 */
.content-wrapper {
    display: flex;
    max-width: 1200px;
    margin: 20px auto;
    gap: 20px;
}

/* 좌측 정보 영역 */
.left-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

/* 컨테이너 공통 */
.container {
    background-color: white;
    border: 1px solid #ccc;
    border-radius: 6px;
    height: 600px; /* 2배 높이 */
    box-sizing: border-box;
    padding: 15px;
    display: flex;
    flex-direction: column;
}

/* Fcontainer 최외각 회색 배경과 연한 하늘색 테두리 */
.Fcontainer {
    background-color: #f0f4f8; /* 밝은 회색 바탕 */
    border: 1px solid #a8c7e7; /* 연한 하늘색 테두리 */
}

/* top-section은 가로 정렬 */
.top-section {
    display: flex;
    flex: 1 1 auto;
    gap: 20px;
}

/* 이미지 영역 - 가로 1.7배 비율 */
.image-area {
    flex: 1.7;
    height: 100%;
    overflow: hidden;
    border-radius: 4px;
}

.image-area img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

/* 요약 영역은 남은 공간 */
.summary-area {
    flex: 1;
    background-color: white; /* 기본 하얀색 유지 */
    border-radius: 4px;
    padding: 10px;
    box-sizing: border-box;
}

/* summary-area 안 ul 스타일 */
.summary-area ul {
    margin: 0;
    padding-left: 20px;
}

.summary-area li {
    margin-bottom: 8px;
    font-size: 1rem;
}

/* description-area는 top-section 아래 */
.description-area {
    margin-top: 15px;
    background-color: white; /* 기본 하얀색 유지 */
    padding: 10px;
    border-radius: 4px;
    box-sizing: border-box;
    flex-shrink: 0;
}

/* 오른쪽 건물 목록 */
.right-list {
    width: 320px;
    background-color: #fff;
    border: 1px solid #ccc;
    border-radius: 6px;
    padding: 15px;
    box-sizing: border-box;
    height: fit-content;
    overflow-y: auto;
}

.building-list {
    list-style: none;
    margin: 0;
    padding: 0;
}

.building-list li {
    margin-bottom: 10px;
}

.building-list li a {
    text-decoration: none;
    color: #004080;
    font-weight: 600;
}

.building-list li a:hover {
    text-decoration: underline;
}


.logo-link {
    position: absolute;
    left: 20px;
    top: 50%;
    transform: translateY(-50%);
}

.page-header {
    background-color: #004080;
    color: white;
    padding: 20px;
    text-align: center;
    position: relative;  
}
```

# AI api를 받아와서 구현하기 
https://aistudio.google.com/prompts/new_chat 
- 여기서 api 키를 발급을 받는다 

## app.py (수정) 
```

```

## index.html (수정) 
```

```

## style.css (수정) 
```

```

# 구글 로그인 연동






