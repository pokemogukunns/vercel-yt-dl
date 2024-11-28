import subprocess
import json
import traceback
from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route('/watch')
def watch_video():
    try:
        videoid = request.args.get('v')
        if not videoid:
            return "No video ID provided", 400

        # curlコマンドを実行してAPIデータを取得
        curl_command = [
            "curl", "-s", f"https://thingproxy.freeboard.io/fetch/https://inv.nadeko.net/api/v1/videos/{videoid}"
        ]
        response = subprocess.run(curl_command, capture_output=True, text=True)

        if response.returncode != 0:
            print(f"Error executing curl: {response.stderr}")
            return "Failed to fetch data", 500

        # レスポンスがJSON形式だと仮定して、データを取得
        data = json.loads(response.stdout)

        # 必要なデータを取り出す
        video_data = {
            "title": data.get("title", "No title"),
            "videoId": data.get("videoId", "No videoId"),
            # adaptiveFormatsがリストの場合、最初の要素のURLを取得
            "adaptiveFormatsUrl": data.get("adaptiveFormats", [{}])[0].get("url", "No adaptiveFormats URL"),
            # 同様にformatStreamsがリストの場合
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
            "storyboardWidth": data.get("storyboardWidth", "No author URL"),
            "genreUrl": data.get("author", "No author URL"),
            "authorThumbnails": data.get("url", "No author URL"),
            "authorId": data.get("authorId", "No author URL"),
            "viewCountText": data.get("viewCountText", "No view count text"),
            "viewCount": data.get("viewCount", "No view count"),
            "quality": data.get("quality", "No quality"),
            "publishedText": data.get("publishedText", "No published text"),
            "published": data.get("published", "No published date"),
        }

        #
        # video.htmlテンプレート(動的にHTMLを変更)
        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{{ title }}</title>
        </head>
        <body>
        <div class="pure-u-1 pure-u-md-12-24 searchbar">
                <form class="pure-form" action="./search" method="get">
                    <fieldset>
                        <input type="search" id="searchbox" autocomplete="on" autocorrect="on" autocapitalize="none" spellcheck="false" autofocus="" name="q" placeholder="検索" title="検索" value="">
                    </fieldset>
                </form>
            </div>
            <video style="outline:none;width:100%;background-color:#000;" playsinline="" poster="https://img.youtube.com/vi/{{ videoId }}/0.jpg" controls="" loadedmetadata="settime()" loop="">
            <source src="{{ formatStreamsUrl }}">
            </video><br>
            <h1>{{ title }}</h1><br>
            <p><strong>Video ID:</strong> {{ videoId }}</p><br>
            <p><strong>概要欄</strong>{{ storyboardWidth }}</p><br>
            <a href="{{ adaptiveFormatsUrl }}">音声をダウンロード</a><br>
            <a href="{{ formatStreamsUrl }}">動画をダウンロード</a><br>
            <img src="{{ url }}"> <a href="/channel?c={{ authorId }}">{{ author }}</a><br>
            <p><strong>視聴数:</strong> {{ viewCount }} 回視聴</p><br>
            <p><strong>画質:</strong> {{ quality }}</p><br>
            <p><strong>公開日：</strong> {{ publishedText }} ({{ published }})</p><br>
               <ul>
            {% for video in recommendedVideos %}
                <li>
                    <strong></strong> <a href="./watch?v={{ video.videoId }}">
                    <img src="https://img.youtube.com/vi/{{ video.videoId }}/0.jpg" /><br>
                    <strong></strong> {{ video.title }}<br></a>
                    <strong></strong> <a href="./channel?c={{ authorId }}">{{ video.author }}</a><br>
                    <strong></strong> {{ video.viewCountText }} ({{ video.viewCount }} views)
                </li>
            {% else %}
                <li>利用可能な推奨ビデオはありません。</li>
            {% endfor %}
            </ul><br>
            
        </body>
        </html>
        """

        # テンプレートをレンダリングして返す
        return render_template_string(html_template, **video_data)
     
    
    except Exception as e:
        # 詳細なエラーメッセージとスタックトレースをログに出力
        print(f"エラーが発生しました: {e}")
        print("Stack trace:", traceback.format_exc())
        return "内部サーバーエラー https://inv.nadeko.net/ がAPIとして機能することを確認し、もう一度読み込み直してください。shortは見れないものが多いです。", 500





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
            "authorBannerUrl": data.get("authorBanners", [{}])[0].get("url", "No banner URL"),
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
        </body>
        </html>
        """

        # テンプレートをレンダリングして返す
        return render_template_string(html_template, query=query, search_results=search_results)

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Stack trace:", traceback.format_exc())
        return "内部サーバーエラー https://inv.nadeko.net/ がAPIとして機能することを確認し、もう一度読み込み直してください。shortは見れないものが多いです。", 500


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
