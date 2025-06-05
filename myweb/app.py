import os
import secrets
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import google.generativeai as genai
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv 
from flask_migrate import Migrate
from jinja2 import TemplateNotFound
from sqlalchemy import MetaData

# .env 파일 로드
load_dotenv()

# 명명 규칙 정의 (제약 조건 이름 문제 해결)
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# .env 파일에서 시크릿 키를 로드합니다.
app.secret_key = os.getenv('SECRET_KEY')
if not app.secret_key:
    # 개발 환경에서만 자동 생성 (프로덕션에서는 반드시 .env에 설정)
    app.secret_key = secrets.token_hex(24)
    print("WARNING: SECRET_KEY가 설정되지 않아 임시 키를 생성했습니다. 프로덕션에서는 .env 파일에 SECRET_KEY를 설정하세요.")

# 명명 규칙을 적용한 메타데이터 생성
db = SQLAlchemy(app, metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate(app, db, render_as_batch=True)  # render_as_batch=True 추가

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Google OAuth 2.0 설정
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# 보안상 민감한 정보는 로그에 출력하지 않음
if GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET:
    print("DEBUG: Google OAuth credentials loaded successfully")
else:
    print("WARNING: Google OAuth credentials not found in environment variables")

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

oauth = OAuth(app)

if GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET:
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={'scope': 'openid email profile'},
    )

# Gemini API 키 설정
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
if GENAI_API_KEY:
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
else:
    print("WARNING: GENAI_API_KEY not found in environment variables")
    model = None

# 데이터베이스 모델 정의
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=True)
    google_id = db.Column(db.String(120), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 관계 정의 (backref 사용)
    posts = db.relationship('Post', backref='author', lazy=True, cascade='all, delete-orphan')
    bulletin_posts = db.relationship('BulletinPost', backref='author', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'

class Post(db.Model):
    __tablename__ = 'post'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # 댓글 관계
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Post {self.title}>'

class BulletinPost(db.Model):
    __tablename__ = 'bulletin_post'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # 댓글 관계
    comments = db.relationship('Comment', backref='bulletin_post', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<BulletinPost {self.title}>'

class Comment(db.Model):
    __tablename__ = 'comment'
    
    id = db.Column(db.Integer, primary_key=True)m
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 외래 키 - 둘 중 하나만 값을 가짐
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)
    bulletin_post_id = db.Column(db.Integer, db.ForeignKey('bulletin_post.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Comment {self.id}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 라우트 정의
@app.route('/')
def index():
    try:
        recent_posts = BulletinPost.query.order_by(BulletinPost.date_posted.desc()).limit(5).all()
        return render_template('index.html', recent_posts=recent_posts, current_user=current_user)
    except Exception as e:
        print(f"Error in index route: {e}")
        return render_template('index.html', recent_posts=[], current_user=current_user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # 입력 검증
        if not username or not password:
            return render_template('register.html', error="사용자 이름과 비밀번호를 모두 입력해주세요.")
        
        if len(username) < 3:
            return render_template('register.html', error="사용자 이름은 3자 이상이어야 합니다.")
        
        if len(password) < 6:
            return render_template('register.html', error="비밀번호는 6자 이상이어야 합니다.")
        
        try:
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                return render_template('register.html', error="이미 사용 중인 사용자 이름입니다.")
            
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Registration error: {e}")
            db.session.rollback()
            return render_template('register.html', error="회원가입 중 오류가 발생했습니다.")
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            return render_template('login.html', error="사용자 이름과 비밀번호를 입력해주세요.")
        
        try:
            user = User.query.filter_by(username=username).first()
            if user and user.password and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                return render_template('login.html', error="사용자 이름 또는 비밀번호가 올바르지 않습니다.")
        except Exception as e:
            print(f"Login error: {e}")
            return render_template('login.html', error="로그인 중 오류가 발생했습니다.")
    
    return render_template('login.html')

@app.route('/login/google')
def google_login():
    if not (GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET):
        return "Google OAuth가 설정되지 않았습니다.", 500
    
    redirect_uri = url_for('google_authorize', _external=True)
    nonce = secrets.token_urlsafe(16)
    session['nonce'] = nonce
    return oauth.google.authorize_redirect(redirect_uri, nonce=nonce)

@app.route('/callback')
def google_authorize():
    if not (GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET):
        return "Google OAuth가 설정되지 않았습니다.", 500
    
    try:
        print(f"\n--- Google OAuth Callback Debug ---")
        token = oauth.google.authorize_access_token()
        print(f"DEBUG: Token acquired successfully")

        nonce = session.get('nonce')
        user_info = oauth.google.parse_id_token(token, nonce=nonce)
        print(f"DEBUG: ID token parsed successfully")

        google_id = user_info.get('sub')
        user = User.query.filter_by(google_id=google_id).first()

        if not user:
            email = user_info.get('email')
            name = user_info.get('name', '')
            username_candidate = email.split('@')[0] if email else f"google_user_{google_id}"
            
            # 사용자명 중복 확인
            counter = 1
            username = username_candidate
            while User.query.filter_by(username=username).first():
                username = f"{username_candidate}_{counter}"
                counter += 1

            user = User(
                username=username,
                google_id=google_id,
                email=email,
                profile_picture=user_info.get('picture')
            )
            db.session.add(user)
            db.session.commit()
            print(f"DEBUG: New user created: {user.username}")

        login_user(user)
        print(f"DEBUG: User logged in successfully: {user.username}")
        print(f"--- Google OAuth Callback Debug End ---\n")
        return redirect(url_for('index'))

    except Exception as e:
        print(f"CRITICAL ERROR during Google OAuth callback: {e}")
        return "Google 로그인 중 오류가 발생했습니다.", 500

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/board')
@login_required
def board():
    try:
        posts = Post.query.order_by(Post.date_posted.desc()).all()
        return render_template('board.html', posts=posts)
    except Exception as e:
        print(f"Error in board route: {e}")
        return render_template('board.html', posts=[])

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        
        if not title or not content:
            return render_template('new_post.html', error="제목과 내용을 모두 입력해주세요.")
        
        try:
            post = Post(title=title, content=content, author=current_user)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('board'))
        except Exception as e:
            print(f"Error creating post: {e}")
            db.session.rollback()
            return render_template('new_post.html', error="게시글 작성 중 오류가 발생했습니다.")
    
    return render_template('new_post.html')

@app.route('/post/<int:post_id>')
def view_post(post_id):
    try:
        post = Post.query.get_or_404(post_id)
        return render_template('view.html', post=post)
    except Exception as e:
        print(f"Error viewing post {post_id}: {e}")
        return "게시글을 찾을 수 없습니다.", 404

@app.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    try:
        post = Post.query.get_or_404(post_id)
        if post.author != current_user:
            return '접근 권한이 없습니다.', 403
        
        if request.method == 'POST':
            title = request.form.get('title', '').strip()
            content = request.form.get('content', '').strip()
            
            if not title or not content:
                return render_template('edit_post.html', post=post, error="제목과 내용을 모두 입력해주세요.")
            
            post.title = title
            post.content = content
            db.session.commit()
            return redirect(url_for('view_post', post_id=post.id))
        
        return render_template('edit_post.html', post=post)
    except Exception as e:
        print(f"Error editing post {post_id}: {e}")
        return "게시글 수정 중 오류가 발생했습니다.", 500

@app.route('/post/delete/<int:post_id>')
@login_required
def delete_post(post_id):
    try:
        post = Post.query.get_or_404(post_id)
        if post.author != current_user:
            return '접근 권한이 없습니다.', 403
        
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('board'))
    except Exception as e:
        print(f"Error deleting post {post_id}: {e}")
        db.session.rollback()
        return "게시글 삭제 중 오류가 발생했습니다.", 500

@app.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    try:
        post = Post.query.get_or_404(post_id)
        content = request.form.get('content', '').strip()
        
        if content:
            comment = Comment(content=content, post_id=post.id, author=current_user)
            db.session.add(comment)
            db.session.commit()
        
        return redirect(url_for('view_post', post_id=post_id))
    except Exception as e:
        print(f"Error adding comment to post {post_id}: {e}")
        db.session.rollback()
        return redirect(url_for('view_post', post_id=post_id))

@app.route('/bulletin')
def bulletin_board():
    try:
        posts = BulletinPost.query.order_by(BulletinPost.date_posted.desc()).all()
        return render_template('bulletin_board.html', posts=posts)
    except Exception as e:
        print(f"Error in bulletin board route: {e}")
        return render_template('bulletin_board.html', posts=[])

@app.route('/bulletin/new', methods=['GET', 'POST'])
@login_required
def new_bulletin_post():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        
        if not title or not content:
            return render_template('new_bulletin_post.html', error="제목과 내용을 모두 입력해주세요.")
        
        try:
            post = BulletinPost(title=title, content=content, author=current_user)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('bulletin_board'))
        except Exception as e:
            print(f"Error creating bulletin post: {e}")
            db.session.rollback()
            return render_template('new_bulletin_post.html', error="게시글 작성 중 오류가 발생했습니다.")
    
    return render_template('new_bulletin_post.html')

@app.route('/bulletin/<int:post_id>')
def view_bulletin_post(post_id):
    try:
        post = BulletinPost.query.get_or_404(post_id)
        return render_template('view_bulletin_post.html', post=post)
    except Exception as e:
        print(f"Error viewing bulletin post {post_id}: {e}")
        return "게시글을 찾을 수 없습니다.", 404

@app.route('/bulletin/<int:post_id>/comment', methods=['POST'])
@login_required
def add_bulletin_comment(post_id):
    try:
        post = BulletinPost.query.get_or_404(post_id)
        content = request.form.get('content', '').strip()
        
        if content:
            comment = Comment(content=content, bulletin_post_id=post.id, author=current_user)
            db.session.add(comment)
            db.session.commit()
        
        return redirect(url_for('view_bulletin_post', post_id=post_id))
    except Exception as e:
        print(f"Error adding comment to bulletin post {post_id}: {e}")
        db.session.rollback()
        return redirect(url_for('view_bulletin_post', post_id=post_id))

@app.route('/building/<int:id>')
def building_page(id):
    if not (1 <= id <= 99):
        return "존재하지 않는 건물입니다.", 404
    
    template_name = f'building/B{id:02d}.html'
    try:
        return render_template(template_name)
    except TemplateNotFound:
        return "해당 건물 페이지를 찾을 수 없습니다.", 404
    except Exception as e:
        print(f"Error loading building page {id}: {e}")
        return "페이지 로드 중 오류가 발생했습니다.", 500

@app.route('/gemini-search', methods=['POST'])
def gemini_search():
    if not model:
        return jsonify({'result': 'Gemini API가 설정되지 않았습니다.'}), 500
    
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'result': '검색어를 입력해주세요.'}), 400
        
        response = model.generate_content(query)
        gemini_results = response.text
        return jsonify({'result': gemini_results})
    except Exception as e:
        print(f"Gemini search error: {e}")
        return jsonify({'result': f'Gemini 검색 오류: {str(e)}'}), 500

# 애플리케이션 컨텍스트에서 데이터베이스 테이블 생성
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
    # 프로덕션 배포 시: app.run(host='0.0.0.0', port=8000, debug=False)
