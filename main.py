from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/home')
def index():
    return open('index.html').read()

@app.route('/get-video-data/<video_id>', methods=['GET'])
def get_video_data(video_id):
    # curlコマンドを実行するURL
    import subprocess

# 実行するcurlコマンド
curl_command = "curl https://thingproxy.freeboard.io/fetch/https://inv.nadeko.net/api/v1/videos/{video_id}"

# curlコマンドを実行し、出力を取得
result = subprocess.run(curl_command, shell=True, capture_output=True, text=True)

# 結果を表示
print(result.stdout)

if __name__ == '__main__':
    app.run(debug=True)
