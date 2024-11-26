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
            "recommendedVideos": data.get("recommendedVideos", "No recommended videos"),
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
            <h1>{{ title }}</h1><br>
            <p><strong>Video ID:</strong> {{ videoId }}</p><br>
            <p><strong><a href="{{ adaptiveFormatsUrl }}">音声のみダウンロード</a></strong></p>
            <a href="{{ formatStreamsUrl }}">音声のみダウンロード</a>
            <p><video src="{{ formatStreamsUrl }}"></video></p>
            <p><strong>Recommended Videos:</strong> {{ recommendedVideos }}</p>
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
