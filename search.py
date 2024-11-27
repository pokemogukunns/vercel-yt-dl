from flask import Flask, render_template_string, request
import subprocess
import json
import traceback

app = Flask(__name__)

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
            <h1>Search Results for "{{ query }}"</h1>
            <ul>
            {% for result in search_results %}
                <li>
                    <a href="/watch?v={{ result.videoId }}">
                        <img src="{{ result.videoThumbnail }}" alt="{{ result.title }}">
                        <h3>{{ result.title }}</h3>
                    </a>
                    <p><strong>Author:</strong> <a href="/channel?c={{ result.authorId }}">{{ result.author }}</a></p>
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
        return "Internal Server Error", 500

if __name__ == '__main__':
    app.run(debug=True)
