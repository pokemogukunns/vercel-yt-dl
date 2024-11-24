from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/get-video-data/<video_id>', methods=['GET'])
def get_video_data(video_id):
    # curlコマンドを実行するURL
    url = f"https://thingproxy.freeboard.io/fetch/https://inv.nadeko.net/api/v1/videos/{video_id}"
    
    try:
        # HTTP GETリクエストを送信
        response = requests.get(url)
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"Error: {response.status_code}"}), 500
    except Exception as e:
        return jsonify({"error": f"リクエスト中にエラーが発生しました: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
