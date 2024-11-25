from flask import Flask, request, jsonify
from flask_cors import CORS  # CORSを許可するためのライブラリ
import requests

app = Flask(__name__)

# CORSを全てのオリジンから許可
CORS(app)

@app.route('/')
def index():
    # フロントエンドのHTMLを返す
    return open('index.html').read()

@app.route('/get-video-data/<video_id>', methods=['GET', 'POST'])
def get_video_data(video_id):
    # curlコマンドを実行するURL
    url = f"https://thingproxy.freeboard.io/fetch/https://inv.nadeko.net/api/v1/videos/{video_id}"
    
    try:
        # HTTPリクエストのタイプに応じた処理
        if request.method == 'GET':
            response = requests.get(url)
        elif request.method == 'POST':
            # POSTリクエスト時の処理（必要に応じてデータを扱う）
            data = request.json if request.is_json else request.form.to_dict()
            response = requests.post(url, json=data)

        # ステータスコードを確認して結果を返す
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"Error: {response.status_code}"}), 500

    except Exception as e:
        return jsonify({"error": f"リクエスト中にエラーが発生しました: {str(e)}"}), 500

if __name__ == '__main__':
    # アプリを実行する（CORSはすべてのオリジンを許可）
    app.run(host='0.0.0.0', port=5000, debug=True)
