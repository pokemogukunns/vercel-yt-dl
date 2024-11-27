import subprocess
import json
import traceback
from flask import Flask, render_template_string, request

app = Flask(__name__)

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
            <title>{{ author }} - チャンネル情報</title>
        </head>
        <body>
            <h1>{{ author }}</h1>
            <img src="{{ authorBannerUrl }}" alt="Author Banner" style="width:100%; max-height:300px;"><br>
            <p><strong>チャンネルID:</strong> {{ authorId }}</p><br>
            <p><strong>説明:</strong> {{ description }}</p><br>
            <p><strong>タグ:</strong> {{ tags | join(', ') }}</p><br>
            <h2>最新動画</h2>
            <ul>
            {% for video in latestVideos %}
                <li>
                    <a href="/watch?v={{ video.videoId }}">
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
        return "Internal Server Error", 500


if __name__ == '__main__':
    app.run(debug=True)
