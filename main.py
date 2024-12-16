import subprocess
import json
import traceback
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# 共通のcurlコマンド実行関数
def fetch_data_from_api(url):
    try:
        curl_command = ["curl", "-s", "--compressed", url]
        response = subprocess.run(curl_command, capture_output=True, text=True)
        if response.returncode != 0:
            print(f"Error executing curl: {response.stderr}")
            return None
        return json.loads(response.stdout)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def decode_unicode_escaped_json(data):
    """
    UnicodeエスケープされたJSON文字列をデコードして戻す関数。

    Args:
        data (str or dict): JSON文字列または辞書形式のデータ

    Returns:
        dict: デコードされたJSON辞書
    """
    if isinstance(data, str):
        # JSON文字列の場合、まずパースして辞書に変換
        try:
            data = json.loads(data)
        except json.JSONDecodeError as e:
            print(f"JSONデコードエラー: {e}")
            return None
    # 再エンコードしてデコード
    return json.loads(json.dumps(data, ensure_ascii=False))



@app.route('/watch')
def watch_video():
    videoid = request.args.get('v')
    if not videoid:
        return "No video ID provided", 400

    # データを取得
    url = f"https://thingproxy.freeboard.io/fetch/https://inv.nadeko.net/api/v1/videos/{videoid}"
    data = fetch_data_from_api(url)

    if not data:
        return "Failed to fetch data", 500

    # 必要なデータを抽出
    video_data = {
        "title": data.get("title", "No title"),
        "videoId": data.get("videoId", "No videoId"),
        "description": data.get("description", "No description"),
        "authorId": data.get("authorId", "No author"),
        "author": data.get("author", "No author"),
        "authorThumbnails": data.get("authorThumbnails", [{}])[0].get("url", "No authorThumbnails URL"),
        "adaptiveFormatsUrl": data.get("adaptiveFormats", [{}])[0].get("url", "No adaptiveFormats URL"),
        "formatStreamsUrl": data.get("formatStreams", [{}])[0].get("url", "No formatStreams URL"),
        "recommendedVideos": [
            {
                "videoId": item.get("videoId", "No videoId"),
                "title": item.get("title", "No title"),
                "author": item.get("author", "No author"),
                "authorUrl": item.get("authorUrl", "No author URL"),
                "viewCountText": item.get("viewCountText", "No view count text"),
                "viewCount": item.get("viewCount", "No view count")
            }
            for item in data.get("recommendedVideos", [])
        ],
        "viewCountText": data.get("viewCountText", "No view count text"),
        "viewCount": data.get("viewCount", "No view count"),
        "quality": data.get("quality", "No quality"),
        "publishedText": data.get("publishedText", "No published text"),
        "published": data.get("published", "No published date"),
    }

    # 動的HTMLテンプレート
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ title }}</title>
        <link rel="stylesheet" href="https://pokemogukunns.github.io/yuki-math/css/empty.css">
        <script src="https://code.jquery.com/jquery-3.5.1.js"></script>
    </head>
    <body>
        <form class="pure-form" action="./search" method="get">
                    <fieldset>
                        <input type="search" id="searchbox" autocomplete="on" autocorrect="on" autocapitalize="none" spellcheck="false" autofocus="" name="q" placeholder="検索" title="検索" value="">
                    </fieldset>
                </form>
        <video width="100%" controls poster="https://img.youtube.com/vi/{{ videoId }}/0.jpg">
            <source src="{{ formatStreamsUrl }}">
        </video>
        <h1>{{ title }}</h1>
        <p><strong>Video ID:</strong><a href="./watch?v={{ videoId }}">{{ videoId }}</a></p>
        <a href="./watch?v={{ videoId }}#log">ログ</a>
        <p><strong>Description:</strong> {{ description }}</p>
        <p><strong>View Count:</strong> {{ viewCount }} views</p>
        <p><strong>Quality:</strong> {{ quality }}</p>
        <p><strong>Published:</strong> {{ publishedText }} ({{ published }})</p>
        <a href="{{ adaptiveFormatsUrl }}">Download 音声</a><br>
        <a href="{{ formatStreamsUrl }}">Download 動画</a><br>
        <a href="/channel?c={{ authorId }}">{{ author }}</a><br>

        <h3>おすすめ動画:</h3>
        <ul>
        {% for video in recommendedVideos %}
            <li><a href="/watch?v={{ video.videoId }}">
            <img src="https://img.youtube.com/vi/{{ video.videoId }}/0.jpg">{{ video.title }}</a> <br> {{ video.author }} ({{ video.viewCountText }})</li>
        {% else %}
            <li>No recommended videos available.</li>
        {% endfor %}
        </ul>
        <div id="log">
        <iframe width="300" height="200" src="./api?v={{ videoId }}"></iframe><br>
<iframe width="500" height="600" src="https://tech-unlimited.com/urlencode.html"></iframe><br>
<iframe width="500" height="600" src="https://tech-unlimited.com/escape.html"></iframe><br>
<iframe width="500" height="600" src="https://tech-unlimited.com/escape-unicode.html"></iframe><br>
<iframe width="500" height="600" src="https://tech-unlimited.com/numeric-char-ref.html"></iframe><br>

    </body>
    </html>
    """

    return render_template_string(html_template, **video_data)


@app.route('/api')
def watch_api():
    apiid = request.args.get('v')
    if not apiid:
        return jsonify({"error": "No video ID provided"}), 400

    # データを取得
    url = f"https://thingproxy.freeboard.io/fetch/https://inv.nadeko.net/api/v1/videos/{apiid}"
    data = fetch_data_from_api(url)

    if not data:
        return jsonify({"error": "Failed to fetch data"}), 500

    # 必要なデータを抽出
    api_data = {
        "title": data.get("title", "No title"),
        "videoId": data.get("videoId", "No videoId"),
        "viewCountText": data.get("viewCountText", "No view count text"),
        "viewCount": data.get("viewCount", "No view count"),
        "recommendedVideos": [
            {
                "videoId": item.get("videoId", "No videoId"),
                "title": item.get("title", "No title"),
                "author": item.get("author", "No author"),
                "authorId": item.get("authorId", "No author"),
                "authorUrl": item.get("authorUrl", "No author URL"),
                "viewCountText": item.get("viewCountText", "No view count text"),
                "viewCount": item.get("viewCount", "No view count")
            }
            for item in data.get("recommendedVideos", [])
        ]
    }

    return jsonify(api_data)


@app.route('/home')
def watch_jp():
    la_id = request.args.get('la')
    if not la_id:
        return "No channel ID provided", 400

    # トレンドデータを取得
    url = f"https://thingproxy.freeboard.io/fetch/https://inv.nadeko.net/api/v1/trending?region={la_id}"
    data = fetch_data_from_api(url)

    if not data:
        return "Failed to fetch trending data", 500

    trending_videos = [
        {
            "title": item.get("title", "No title"),
            "videoId": item.get("videoId", "No videoId"),
            "author": item.get("author", "No author"),
            "authorId": item.get("authorId", "No authorId"),
            "videoThumbnail": item.get("videoThumbnails", [{}])[0].get("url", "No thumbnail URL"),
            "viewCountText": item.get("viewCountText", "No view count text"),
            "publishedText": item.get("publishedText", "No published text"),
            "lengthSeconds": item.get("lengthSeconds", "No length")
        }
        for item in data.get("items", [])
    ]

    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>トレンドビデオ</title>
    </head>
    <body>
        <h3>Trending Videos:</h3>
        <ul>
        {% for video in trending_videos %}
            <li>
                <a href="/watch?v={{ video.videoId }}">
                    <img src="{{ video.videoThumbnail }}" alt="{{ video.title }}">
                    <h3>{{ video.title }}</h3>
                </a>
                <p>Author: <a href="/channel?c={{ video.authorId }}">{{ video.author }}</a></p>
                <p>View Count: {{ video.viewCountText }}</p>
                <p>Published: {{ video.publishedText }}</p>
                <p>Length: {{ video.lengthSeconds }} seconds</p>
            </li>
        {% else %}
            <li>No trending videos available.</li>
        {% endfor %}
        </ul>
    </body>
    </html>
    """

    return render_template_string(html_template, trending_videos=trending_videos)

@app.route('/channel')
def channel_page():
    try:
        # チャンネルIDを取得
        channel_id = request.args.get('c')
        if not channel_id:
            return "No channel ID provided", 400

        # curlコマンドを実行してチャンネルデータを取得
        curl_command = [
            "curl", "-s", f"https://thingproxy.freeboard.io/fetch/https://inv.nadeko.net/api/v1/channels/{channel_id}"
        ]
        response = subprocess.run(curl_command, capture_output=True, text=True)

        if response.returncode != 0:
            print(f"Error executing curl: {response.stderr}")
            return "Failed to fetch data", 500

        # JSONレスポンスを解析
        try:
            data = json.loads(response.stdout)
        except json.JSONDecodeError:
            print(f"Invalid JSON response: {response.stdout}")
            return "Invalid response from API", 500

        # 必要なデータを抽出
        channel_data = {
            "author": data.get("author", "No author"),
            "authorId": data.get("authorId", "No authorId"),
            "authorBannerUrl": data.get("authorBanners", [{}])[0].get("url", "https://pokemogukunns.github.io/no-channel-img.png") if data.get("authorBanners") else "https://pokemogukunns.github.io/no-channel-img.png",
            "description": data.get("description", "No description"),
            "tags": data.get("tags", []),
            "latestVideos": [
                {
                    "title": video.get("title", "No title"),
                    "videoId": video.get("videoId", "No videoId"),
                    "description": video.get("description", "No description"),
                    "viewCountText": video.get("viewCountText", "No view count text"),
                    "publishedText": video.get("publishedText", "No published date"),
                }
                for video in data.get("latestVideos", [])
            ],
        }

        # チャンネル情報テンプレート
        html_template = """
        <!DOCTYPE html>
        <html lang="ja">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{{ author }}</title>
        </head>
        <body>
        <div class="pure-u-1 pure-u-md-12-24 searchbar">
                <form class="pure-form" action="./search" method="get">
                    <fieldset>
                        <input type="search" id="searchbox" autocomplete="on" autocorrect="on" autocapitalize="none" spellcheck="false" autofocus="" name="q" placeholder="検索" title="検索" value="">
                    </fieldset>
                </form>
            </div>
            <h1>{{ author }}</h1>
            <img src="{{ authorBannerUrl }}" alt="Author Banner" style="width:100%; max-height:300px;"><br>
            <p><strong>チャンネルID:</strong> {{ authorId }}</p><br>
            <p><strong>説明:</strong> {{ description }}</p><br>
            <p><strong>タグ:</strong> {{ tags | join(', ') }}</p><br>
            <h2>最新動画</h2>
            <ul>
            {% for video in latestVideos %}
                <li>
                    <a href="./watch?v={{ video.videoId }}">
                    <img src="https://img.youtube.com/vi/{{ video.videoId }}/0.jpg" />
                        <h3>{{ video.title }}</h3>
                        <p>{{ video.description }}</p>
                        <p><strong>視聴数:</strong> {{ video.viewCountText }}</p>
                        <p><strong>公開日:</strong> {{ video.publishedText }}</p>
                    </a>
                </li>
            {% else %}
                <li>動画が見つかりません。</li>
            {% endfor %}
            </ul>
            {{ json_data }}
        </body>
        </html>
        """

        # テンプレートをレンダリングして返す
        return render_template_string(html_template, **channel_data)

    except Exception as e:
        # 詳細なエラーメッセージとスタックトレースをログに出力
        print(f"An error occurred: {e}")
        print("Stack trace:", traceback.format_exc())
        return "内部サーバーエラー https://inv.nadeko.net/ がAPIとして機能することを確認し、もう一度読み込み直してください。shortは見れないものが多いです。", 500



@app.route('/search')
def search_videos():
    try:
        query = request.args.get('q')
        if not query:
            return "No search query provided", 400

        # curlコマンドを実行してAPIデータを取得
        curl_command = [
            "curl", "-s", f"https://thingproxy.freeboard.io/fetch/https://inv.nadeko.net/api/v1/search?q={query}"
        ]
        response = subprocess.run(curl_command, capture_output=True, text=True)

        if response.returncode != 0:
            print(f"Error executing curl: {response.stderr}")
            return "Failed to fetch search results", 500

        # レスポンスがJSON形式だと仮定して、データを取得
        data = json.loads(response.stdout)

        # データ形式がリストの場合に対応
        if isinstance(data, list):
            search_results = [
                {
                    "title": item.get("title", "No title"),
                    "videoId": item.get("videoId", "No videoId"),
                    "author": item.get("author", "No author"),
                    "authorId": item.get("authorId", "No authorId"),
                    "videoThumbnail": item.get("videoThumbnails", [{}])[0].get("url", "No thumbnail URL"),
                    "viewCountText": item.get("viewCountText", "No view count text"),
                    "publishedText": item.get("publishedText", "No published text"),
                    "lengthSeconds": item.get("lengthSeconds", "No length")
                }
                for item in data
            ]
        else:
            search_results = []

        # 動的なHTMLテンプレート
        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Search Results</title>
        </head>
        <body>
        <div class="pure-u-1 pure-u-md-12-24 searchbar">
                <form class="pure-form" action="./search" method="get">
                    <fieldset>
                        <input type="search" id="searchbox" autocomplete="on" autocorrect="on" autocapitalize="none" spellcheck="false" autofocus="" name="q" placeholder="検索" title="検索" value="">
                    </fieldset>
                </form>
            </div>
            <h1>検索結果 "{{ query }}"</h1>
            <ul>
            {% for result in search_results %}
                <li>
                    <a href="./watch?v={{ result.videoId }}">
                        <img src="https://img.youtube.com/vi/{{ result.videoId }}/0.jpg" alt="{{ result.title }}">
                        <h3>{{ result.title }}</h3>
                    </a>
                    <p><strong>Author:</strong> <a href="./channel?c={{ result.authorId }}">{{ result.author }}</a></p>
                    <p><strong>View Count:</strong> {{ result.viewCountText }}</p>
                    <p><strong>Published:</strong> {{ result.publishedText }}</p>
                    <p><strong>Length:</strong> {{ result.lengthSeconds }} seconds</p>
                </li>
            {% endfor %}
            </ul>
            {{ json_data }}
        </body>
        </html>
        """

        # テンプレートをレンダリングして返す
        return render_template_string(html_template, query=query, search_results=search_results)

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Stack trace:", traceback.format_exc())
        return "内部サーバーエラー https://inv.nadeko.net/ がAPIとして機能することを確認し、もう一度読み込み直してください。shortは見れないものが多いです。", 500




if __name__ == '__main__':
    app.run(debug=True)
