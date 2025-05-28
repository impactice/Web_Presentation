import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import google.generativeai as genai
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# .env 파일에서 시크릿 키를 로드합니다.
app.secret_key = os.getenv('SECRET_KEY')
if not app.secret_key:
    raise ValueError("SECRET_KEY 환경 변수가 설정되지 않았습니다. .env 파일을 확인하세요. (예: python -c \"import os; print(os.urandom(24).hex())\" 로 생성)")

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Google OAuth 2.0 설정
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# 디버깅: 클라이언트 ID와 시크릿이 제대로 로드되었는지 확인 (서버 시작 시 터미널에 출력됨)
print(f"DEBUG: Loaded GOOGLE_CLIENT_ID: {'*' * (len(GOOGLE_CLIENT_ID) - 10) + GOOGLE_CLIENT_ID[-10:] if GOOGLE_CLIENT_ID else 'None'}")
print(f"DEBUG: Loaded GOOGLE_CLIENT_SECRET: {'*' * (len(GOOGLE_CLIENT_SECRET) - 5) if GOOGLE_CLIENT_SECRET else 'None'}")


CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

oauth = OAuth(app)

oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url=CONF_URL,
    client_kwargs={'scope': 'openid email profile'},
)

# Gemini API 키 설정 (안전하게 관리해야 함!)
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
genai.configure(api_key=GENAI_API_KEY)

MODEL_NAME = "gemini-1.5-flash"
generation_config = {
    "temperature": 0.9,
    "top_p": 1.0
}
safety_settings = [
    {"category": "harassment", "threshold": "block_medium_and_above"},
    {"category": "hate_speech", "threshold": "block_medium_and_above"},
    {"category": "sexually_explicit", "threshold": "block_medium_and_above"}
]
model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    generation_config=generation_config,
    safety_settings=safety_settings
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=True)
    google_id = db.Column(db.String(120), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='user_posts', lazy=True)
    # comments = db.relationship('Comment', backref='user_comments', lazy=True) # 아래 Comment 모델에서 author 관계가 있으므로 제거
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
    # 이 부분은 변경하지 않습니다. Post에서 Comment로의 1-to-many 관계의 "one" 쪽입니다.
    comments = db.relationship('Comment', backref='post_comments', cascade='all, delete-orphan', lazy=True) # <-- 이 backref 이름을 'comments'로 바꾸는게 더 직관적이지만 일단 유지

    def __repr__(self):
        return f'<Post {self.title}>'

# BulletinPost 모델에 comments backref 명시적으로 추가 (옵션: 가독성 향상)
class BulletinPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref='written_bulletin_posts', lazy=True)
    # BulletinPost에서 Comment로의 1-to-many 관계의 "one" 쪽입니다.
    comments = db.relationship('Comment', backref='bulletin_post_comments', cascade='all, delete-orphan', lazy=True)


    def __repr__(self):
        return f'<BulletinPost {self.title}>'


# Comment 모델을 이렇게 수정해야 합니다:
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)
    bulletin_post_id = db.Column(db.Integer, db.ForeignKey('bulletin_post.id'), nullable=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # 여기서 cascade='all, delete-orphan'을 제거합니다.
    # Comment는 Post/BulletinPost에 대한 "many" 쪽이므로 cascade를 설정하지 않습니다.
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

@app.route('/login/google')
def google_login():
    redirect_uri = url_for('google_authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

# --- 수정된 Google 로그인 콜백 처리 부분 (nonce 추가) ---
@app.route('/callback')
def google_authorize():
    try:
        # 이 단계에서 문제가 발생하는지 확인하기 위해 각 호출 전후에 print 추가
        print(f"\n--- Google OAuth Callback Debug ---")
        print(f"DEBUG: Attempting to authorize access token...")
        token = oauth.google.authorize_access_token() # 이 줄에서 오류가 발생할 가능성 높음
        print(f"DEBUG: Token acquired: {token}")

        print(f"DEBUG: Attempting to parse ID token...")
        # Authlib 1.0.0 이상에서는 nonce를 parse_id_token()에 명시적으로 전달해야 함
        # nonce는 authorize_redirect()에서 Authlib이 세션에 자동으로 저장함
        user_info = oauth.google.parse_id_token(token, nonce=session.get('nonce')) # <-- 이 부분 수정!
        print(f"DEBUG: ID token parsed: {user_info}")

        # 나머지 디버깅 print 문 및 로직은 그대로 유지
        print(f"    - Google ID (sub): {user_info.get('sub')}")
        print(f"    - Email: {user_info.get('email')}")
        print(f"    - Name: {user_info.get('name')}")
        print(f"    - Profile Picture: {user_info.get('picture')}")

        google_id = user_info.get('sub')
        user = User.query.filter_by(google_id=google_id).first()
        print(f"DEBUG: User lookup by google_id '{google_id}': {'Found' if user else 'Not Found'}")

        if not user:
            email = user_info.get('email')
            username_candidate = email if email else f"google_user_{google_id}"
            existing_user_by_username = User.query.filter_by(username=username_candidate).first()
            existing_user_by_email = User.query.filter_by(email=email).first()

            print(f"DEBUG: New user path: Proposed username: '{username_candidate}'")
            if existing_user_by_username or existing_user_by_email:
                username = f"google_{google_id}"
                print(f"DEBUG: Conflict detected, modified username to: '{username}')")
                if existing_user_by_email and existing_user_by_email.google_id != google_id:
                    email = None
            else:
                username = username_candidate

            user = User(
                username=username,
                google_id=google_id,
                email=email,
                profile_picture=user_info.get('picture')
            )
            db.session.add(user)
            db.session.commit()
            print(f"DEBUG: New user created in DB: {user}")

        login_user(user)
        print(f"DEBUG: User '{user.username}' (ID: {user.id}) logged in successfully via Google.")
        print(f"--- Google OAuth Callback Debug End ---\n")
        return redirect(url_for('index'))

    except Exception as e:
        print(f"\n!!! CRITICAL ERROR during Google OAuth callback: {e} !!!\n")
        raise e

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

@app.route('/gemini-search', methods=['POST'])
def gemini_search():
    data = request.get_json()
    query = data.get('query')
    try:
        response = model.generate_content(query)
        gemini_results = response.text
    except Exception as e:
        gemini_results = f"Gemini 검색 오류: {str(e)}"
    return jsonify({'result': gemini_results})

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=8000, debug=True)