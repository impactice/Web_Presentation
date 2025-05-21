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




