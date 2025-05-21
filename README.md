# pip 다운 
```
pip install flask
```

- 설치 확인
```
python -m flask --version
```

```
pip install Flask-SQLAlchemy
```

# templates 
- board.html
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
