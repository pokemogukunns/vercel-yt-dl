from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/home')
def index():
    return open('index.html').read()

@app.route('/get-video-data/<video_id>', methods=['GET'])
def get_video_data(video_id):
    # curlコマンドを実行するURL
    curl_command = f"curl https://thingproxy.freeboard.io/fetch/https://inv.nadeko.net/api/v1/videos/{video_id}"

    # curlコマンドを実行し、出力を取得
    result = subprocess.run(curl_command, shell=True, capture_output=True, text=True)

    # 結果をJSONとして返す
    if result.returncode == 0:
        # 成功した場合は、結果をJSONで返す
        return jsonify({"data": result.stdout})
    else:
        # エラーが発生した場合は、エラーメッセージを返す
        return jsonify({"error": "Failed to fetch data"}), 500

if __name__ == '__main__':
    app.run(debug=True)

