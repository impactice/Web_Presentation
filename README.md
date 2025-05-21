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
# 파일 전체 흐름
```
myweb/
├── app.py
├── .env
├── templates/
│   ├── index.html
│   ├── bulletin_board.html
│   ├── edit_post.html
│   ├── login.html
│   ├── new_bulletin_post.html
│   ├── new_post.html
│   ├── register.html
│   ├── view.html
│   ├── view_bulletin_post.html
│   ├── building/
│   │   ├── B01.html
│   │   ├── B26.html
│   │   └── B27.html
│   └── board.html
├── static/            # 정적 파일
│   ├── buildingC/
│   │   └── B01.css
│   ├── images/
│   │   └── ...
│   ├── board.css
│   ├── bulletin_board.css
│   ├── image_slider.css
│   ├── image_slider.js
│   ├── style.css
│   └── view.css
└── instance/          # 데이터베이스 파일 (database.db)
    └── database.db 
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

- bulletin_board.html
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

- index.html 
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
- login.html 
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

- new_bulletin_post.html

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
- new_post.html
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

# view.html
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
