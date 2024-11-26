import subprocess
import json
import traceback
from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route('/channel')
def watch_video():
    try:
        channelid = request.args.get('c')
        if not videoid:
            return "No video ID provided", 400

        # curlコマンドを実行してAPIデータを取得
        curl_command = [
            "curl", "-s", f"https://thingproxy.freeboard.io/fetch/https://inv.nadeko.net/api/v1/channels/{channelid}"
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
            # latestVideosがリストの場合、各要素から必要なデータを取り出す
            "latestVideos": [
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
            "authorUrl": data.get("authorUrl", "No author URL"),
            "viewCountText": data.get("viewCountText", "No view count text"),
            "viewCount": data.get("viewCount", "No view count"),
            "quality": data.get("quality", "No quality"),
            "publishedText": data.get("publishedText", "No published text"),
            "published": data.get("published", "No published date"),
        }

        # video.htmlテンプレート
        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{{ title }}</title>
        </head>
        <body>
            <h1>{{ title }}</h1>
            <p><strong>Video ID:</strong> {{ videoId }}</p>
            <p><strong>Adaptive Formats URL:</strong> {{ adaptiveFormatsUrl }}</p>
            <p><strong>Format Streams URL:</strong> {{ formatStreamsUrl }}</p>
            <p><strong>Recommended Videos:</strong></p>
            <ul>
            {% for video in latestVideos %}
                <li>
                    <strong>Video ID:</strong> <a href="https://my-vercel.app/watch?v={{ video.videoId }}">{{ video.videoId }}</a><br>
                    <strong>Title:</strong> {{ video.title }}<br>
                    <strong>Author:</strong> <a href="{{ video.authorUrl }}">{{ video.author }}</a><br>
                    <strong>View Count:</strong> {{ video.viewCountText }} ({{ video.viewCount }} views)
                </li>
            {% else %}
                <li>No recommended videos available.</li>
            {% endfor %}
            </ul>
            <p><strong>Author URL:</strong> <a href="{{ authorUrl }}">{{ authorUrl }}</a></p>
            <p><strong>View Count:</strong> {{ viewCountText }} ({{ viewCount }} views)</p>
            <p><strong>Quality:</strong> {{ quality }}</p>
            <p><strong>Published Date:</strong> {{ publishedText }} ({{ published }})</p>
        </body>
        </html>
        """

        # テンプレートをレンダリングして返す
        return render_template_string(html_template, **video_data)

    except Exception as e:
        # 詳細なエラーメッセージとスタックトレースをログに出力
        print(f"An error occurred: {e}")
        print("Stack trace:", traceback.format_exc())
        return "Internal Server Error", 500

if __name__ == '__main__':
    app.run(debug=True)
