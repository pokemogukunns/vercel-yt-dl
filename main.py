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
            {{ json_data }}
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







@app.route('/api')
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
        #
{
  "type": "video",
  "title": "{{ title }}",
  "videoId": "b0tbxShxFws",
  "videoThumbnails": [
    {
      "quality": "maxres",
      "url": "https://inv.nadeko.net/vi/b0tbxShxFws/maxres.jpg",
      "width": 1280,
      "height": 720
    }
  ],
  "storyboards": [
    {
      "url": "/api/v1/storyboards/b0tbxShxFws?width=320&height=180",
      "templateUrl": "https://i.ytimg.com/sb/b0tbxShxFws/storyboard3_L3/M$M.jpg?sqp=-oaymwENSDfyq4qpAwVwAcABBqLzl_8DBgj2qLqnBg%3D%3D&sigh=rs%24AOn4CLCTH-7GACWwWFKDtSRY8FKFyd9aGg",
      "width": 320,
      "height": 180,
      "count": 152,
      "interval": 10000,
      "storyboardWidth": 3,
      "storyboardHeight": 3,
      "storyboardCount": 17
    }
  ],
  "description": "",
  "descriptionHtml": "",
  "published": 1693267200,
  "publishedText": "1年前",
  "keywords": [],
  "viewCount": 31192,
  "likeCount": 0,
  "dislikeCount": 0,
  "paid": false,
  "premium": false,
  "isFamilyFriendly": true,
  "genre": "Education",
  "genreUrl": null,
  "author": "Eiken Foundation of Japan",
  "authorId": "UCYLj-_GA6hHV0fd6A9pMGow",
  "authorUrl": "/channel/UCYLj-_GA6hHV0fd6A9pMGow",
  "authorVerified": false,
  "authorThumbnails": [
    {
      "url": "https://yt3.ggpht.com/ytc/AIdro_nG_pLAgEPHnWUEYGcnOnzJ08ED9uoCA1O0rURvrZgejA=s32-c-k-c0x00ffffff-no-rj",
      "width": 32,
      "height": 32
    },
  ],
  "subCountText": "7.09K",
  "lengthSeconds": 1509,
  "allowRatings": false,
  "rating": 0,
  "isListed": true,
  "liveNow": false,
  "isPostLiveDvr": false,
  "isUpcoming": false,
  "dashUrl": "https://inv.nadeko.net/api/manifest/dash/id/b0tbxShxFws",
  "adaptiveFormats": [
    {
      "init": "0-631",
      "index": "632-2487",
      "bitrate": "131664",
      "url": "https://rr5---sn-uxgg5-njall.googlevideo.com/videoplayback?expire=1732947479&ei=t1lKZ8T7HcSa-LAP9tXTkAc&ip=186.105.135.2&id=o-AENVfEsZZWhYzdCbUPI-vImVvCghHteANDa15bobFGdu&itag=140&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&met=1732925879%2C&mh=jG&mm=31%2C29&mn=sn-uxgg5-njall%2Csn-uxgg5-njaed&ms=au%2Crdu&mv=m&mvi=5&pl=19&rms=au%2Cau&initcwndbps=2130000&bui=AQn3pFSF0H7g2gyAhdZtd7e04ICfNzC58h7omyEl18gcrwn8lV8EXydUYYfxS1H_M_jCBRn-fAwQfVkQ&spc=qtApAf0U6DX4dAZRvrtzuOGblFhz0Qj-B4SLDpT2qfrIZkp606b30-EpTD0g&vprv=1&svpuc=1&mime=audio%2Fmp4&ns=13kmSTCEkfIMEOYJ_A07a-IQ&rqh=1&gir=yes&clen=24407521&ratebypass=yes&dur=1508.089&lmt=1693560460480545&mt=1732925365&fvip=3&keepalive=yes&fexp=51326932%2C51335594&c=WEB&sefc=1&txp=5318224&n=SGlh7GDJQ7_Iew&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Cns%2Crqh%2Cgir%2Cclen%2Cratebypass%2Cdur%2Clmt&sig=AJfQdSswRAIgZ5s5fKS1rdpeTHYGBmQy92B4Mtg01ws312c1dBqGxyMCIBvr2U2RF12nr6FVaN5WI84RpcF1KdY_yTcNInaADrSP&lsparams=met%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=AGluJ3MwRQIgTZPXykTqCEsa4mW-2L6ba02UkKnBY6L06XqIvWt_oggCIQCzGplfkhGnF8VXYWXc_P_gFMTazE_XSlqx9tnSR9Z6xg%3D%3D&pot=MnRq9bywjIhAa2rNNl4PwaRveWDHtTfryA6TLKmTJalZzwcVWJlWpCM8BcrotpmQWa4JK6nxFZwMVsRVb9N2qwpKt6ZrRzk6jccaztfL9FDByAaSI_JV3_fqCO9gpNFZDaxEiugTg3nqyhlcF-NcuN-nh4z_EA%3D%3D",
      "itag": "140",
      "type": "audio/mp4; codecs=\"mp4a.40.2\"",
      "clen": "24407521",
      "lmt": "1693560460480545",
      "projectionType": "RECTANGULAR",
      "container": "m4a",
      "encoding": "aac",
      "audioQuality": "AUDIO_QUALITY_MEDIUM",
      "audioSampleRate": 44100,
      "audioChannels": 2
    }
  ],
  "formatStreams": [
    {
      "url": "{{ formatStreamsUrl }}",
      "itag": "18",
      "type": "video/mp4; codecs=\"avc1.42001E, mp4a.40.2\"",
      "quality": "medium",
      "bitrate": "466305",
      "fps": 30,
      "size": "640x360",
      "resolution": "360p",
      "qualityLabel": "360p",
      "container": "mp4",
      "encoding": "h264"
    }
  ],
  "recommendedVideos": [
    {
      "videoId": "DQyH7jBD0hY",
      "title": "Learn English quickly with Smart Podcast | Episode 15",
      "videoThumbnails": [
        {
          "quality": "maxres",
          "url": "https://inv.nadeko.net/vi/DQyH7jBD0hY/maxres.jpg",
          "width": 1280,
          "height": 720
        }
      ],
      "author": "English Smart Podcast",
      "authorUrl": "/channel/UCS5SY45nVDDAQTBmPCLGHbQ",
      "authorId": "UCS5SY45nVDDAQTBmPCLGHbQ",
      "authorVerified": false,
      "lengthSeconds": 1013,
      "viewCountText": "94",
      "viewCount": 94
    },
      ],
      "author": "Marisa's English Adventure",
      "authorUrl": "/channel/UCwbcobsHlcpXnCkhIEac6EQ",
      "authorId": "UCwbcobsHlcpXnCkhIEac6EQ",
      "authorVerified": false,
      "lengthSeconds": 355,
      "viewCountText": "659",
      "viewCount": 659
    },
  ]
}

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
            {{ json_data }}
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

























@app.route('/home')
def trending_videos():
    try:
        # `curl`コマンドを使ってAPIデータを取得
        curl_command = [
            "curl", "-s", "https://thingproxy.freeboard.io/fetch/https://inv.nadeko.net/api/v1/trending?region=JP"
        ]
        response = subprocess.run(curl_command, capture_output=True, text=True)

        if response.returncode != 0:
            print(f"Error executing curl: {response.stderr}")
            return "Failed to fetch trending videos", 500

        # レスポンスがJSON形式だと仮定して、データを取得
        data = json.loads(response.stdout)

        # 必要なデータを整形して取得
        trending_videos = [
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
            for item in data.get("items", [])
        ]

        # 動的なHTMLテンプレート
        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Trending Videos</title>
        </head>
        <body>
            <h1>Trending Videos in Japan</h1>
            <ul>
            {% for result in trending_videos %}
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
            {{ json_data }}
        </body>
        </html>
        """

        # テンプレートをレンダリングして返す
        return render_template_string(html_template, trending_videos=trending_videos)

    except Exception as e:
        print(f"An error occurred: {e}")
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
            {{ json_data }}
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
            {{ json_data }}
        </body>
        </html>
        """

        # テンプレートをレンダリングして返す
        return render_template_string(html_template, query=query, search_results=search_results)

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Stack trace:", traceback.format_exc())
        return "内部サーバーエラー https://inv.nadeko.net/ がAPIとして機能することを確認し、もう一度読み込み直してください。shortは見れないものが多いです。", 500



@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
