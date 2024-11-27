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
            <video style="outline:none;width:100%;background-color:#000;" playsinline="" poster="https://img.youtube.com/vi/{{ videoId }}/0.jpg" controls="" loadedmetadata="settime()" loop="">
            <source src="{{ formatStreamsUrl }}">
            </video><br>
            <h1>{{ title }}</h1><br>
            <p><strong>Video ID:</strong> {{ videoId }}</p><br>
            <p><strong>概要欄</strong>{{ storyboardWidth }}</p><br>
            <a href="{{ adaptiveFormatsUrl }}">音声をダウンロード</a><br>
            <a href="{{ formatStreamsUrl }}">動画をダウンロード</a><br>
            <p><strong><img src="{{ url }}"></strong> <a href="/channel?c={{ authorId }}">{{ author }}</a></p><br>
            <p><strong>視聴数:</strong> {{ viewCount }} 回視聴</p><br>
            <p><strong>画質:</strong> {{ quality }}</p><br>
            <p><strong>公開日：</strong> {{ publishedText }} ({{ published }})</p><br>
               <ul>
            {% for video in recommendedVideos %}
                <li>
                    <strong></strong> <a href="https://vercel-tau-lac-41.vercel.app/watch?v={{ video.videoId }}">
                    <img src="https://img.youtube.com/vi/{{ video.videoId }}/0.jpg" /><br>
                    <strong></strong> {{ video.title }}<br></a>
                    <strong></strong> <a href="{{ video.authorUrl }}">{{ video.author }}</a><br>
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
        print(f"An error occurred: {e}")
        print("Stack trace:", traceback.format_exc())
        return "Internal Server Error", 500



if __name__ == '__main__':
    app.run(debug=True)
