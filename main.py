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
        #{"type":"video",
        #"title":"【特別講義】英検を活用して4技能を伸ばそう!ライティング新形式で書く力を育てる方法（安河内哲也先生）","videoId":"b0tbxShxFws","videoThumbnails":[{"quality":"maxres","url":"https://inv.nadeko.net/vi/b0tbxShxFws/maxres.jpg","width":1280,"height":720},{"quality":"maxresdefault","url":"https://inv.nadeko.net/vi/b0tbxShxFws/maxresdefault.jpg","width":1280,"height":720},{"quality":"sddefault","url":"https://inv.nadeko.net/vi/b0tbxShxFws/sddefault.jpg","width":640,"height":480},{"quality":"high","url":"https://inv.nadeko.net/vi/b0tbxShxFws/hqdefault.jpg","width":480,"height":360},{"quality":"medium","url":"https://inv.nadeko.net/vi/b0tbxShxFws/mqdefault.jpg","width":320,"height":180},{"quality":"default","url":"https://inv.nadeko.net/vi/b0tbxShxFws/default.jpg","width":120,"height":90},{"quality":"start","url":"https://inv.nadeko.net/vi/b0tbxShxFws/1.jpg","width":120,"height":90},{"quality":"middle","url":"https://inv.nadeko.net/vi/b0tbxShxFws/2.jpg","width":120,"height":90},{"quality":"end","url":"https://inv.nadeko.net/vi/b0tbxShxFws/3.jpg","width":120,"height":90}],"storyboards":[{"url":"/api/v1/storyboards/b0tbxShxFws?width=48&height=27","templateUrl":"https://i.ytimg.com/sb/b0tbxShxFws/storyboard3_L0/default.jpg?sqp=-oaymwENSDfyq4qpAwVwAcABBqLzl_8DBgj2qLqnBg%3D%3D&sigh=rs%24AOn4CLAGR9ihu3RAqP_LQWyH0R-8kVHaqw","width":48,"height":27,"count":100,"interval":15090,"storyboardWidth":10,"storyboardHeight":10,"storyboardCount":1},{"url":"/api/v1/storyboards/b0tbxShxFws?width=80&height=45","templateUrl":"https://i.ytimg.com/sb/b0tbxShxFws/storyboard3_L1/M$M.jpg?sqp=-oaymwENSDfyq4qpAwVwAcABBqLzl_8DBgj2qLqnBg%3D%3D&sigh=rs%24AOn4CLBXmohczPM1b-P4ICRBdLMrMsZTWg","width":80,"height":45,"count":152,"interval":10000,"storyboardWidth":10,"storyboardHeight":10,"storyboardCount":2},{"url":"/api/v1/storyboards/b0tbxShxFws?width=160&height=90","templateUrl":"https://i.ytimg.com/sb/b0tbxShxFws/storyboard3_L2/M$M.jpg?sqp=-oaymwENSDfyq4qpAwVwAcABBqLzl_8DBgj2qLqnBg%3D%3D&sigh=rs%24AOn4CLDZybVbuKWhGw2dlbgOdcVTTne-cA","width":160,"height":90,"count":152,"interval":10000,"storyboardWidth":5,"storyboardHeight":5,"storyboardCount":7},{"url":"/api/v1/storyboards/b0tbxShxFws?width=320&height=180","templateUrl":"https://i.ytimg.com/sb/b0tbxShxFws/storyboard3_L3/M$M.jpg?sqp=-oaymwENSDfyq4qpAwVwAcABBqLzl_8DBgj2qLqnBg%3D%3D&sigh=rs%24AOn4CLCTH-7GACWwWFKDtSRY8FKFyd9aGg","width":320,"height":180,"count":152,"interval":10000,"storyboardWidth":3,"storyboardHeight":3,"storyboardCount":17}],"description":"","descriptionHtml":"","published":1693267200,"publishedText":"1年前","keywords":[],"viewCount":31192,"likeCount":0,"dislikeCount":0,"paid":false,"premium":false,"isFamilyFriendly":true,"allowedRegions":["AD","AE","AF","AG","AI","AL","AM","AO","AQ","AR","AS","AT","AU","AW","AX","AZ","BA","BB","BD","BE","BF","BG","BH","BI","BJ","BL","BM","BN","BO","BQ","BR","BS","BT","BV","BW","BY","BZ","CA","CC","CD","CF","CG","CH","CI","CK","CL","CM","CN","CO","CR","CU","CV","CW","CX","CY","CZ","DE","DJ","DK","DM","DO","DZ","EC","EE","EG","EH","ER","ES","ET","FI","FJ","FK","FM","FO","FR","GA","GB","GD","GE","GF","GG","GH","GI","GL","GM","GN","GP","GQ","GR","GS","GT","GU","GW","GY","HK","HM","HN","HR","HT","HU","ID","IE","IL","IM","IN","IO","IQ","IR","IS","IT","JE","JM","JO","JP","KE","KG","KH","KI","KM","KN","KP","KR","KW","KY","KZ","LA","LB","LC","LI","LK","LR","LS","LT","LU","LV","LY","MA","MC","MD","ME","MF","MG","MH","MK","ML","MM","MN","MO","MP","MQ","MR","MS","MT","MU","MV","MW","MX","MY","MZ","NA","NC","NE","NF","NG","NI","NL","NO","NP","NR","NU","NZ","OM","PA","PE","PF","PG","PH","PK","PL","PM","PN","PR","PS","PT","PW","PY","QA","RE","RO","RS","RU","RW","SA","SB","SC","SD","SE","SG","SH","SI","SJ","SK","SL","SM","SN","SO","SR","SS","ST","SV","SX","SY","SZ","TC","TD","TF","TG","TH","TJ","TK","TL","TM","TN","TO","TR","TT","TV","TW","TZ","UA","UG","UM","US","UY","UZ","VA","VC","VE","VG","VI","VN","VU","WF","WS","YE","YT","ZA","ZM","ZW"],"genre":"Education","genreUrl":null,"author":"Eiken Foundation of Japan","authorId":"UCYLj-_GA6hHV0fd6A9pMGow","authorUrl":"/channel/UCYLj-_GA6hHV0fd6A9pMGow","authorVerified":false,"authorThumbnails":[{"url":"https://yt3.ggpht.com/ytc/AIdro_nG_pLAgEPHnWUEYGcnOnzJ08ED9uoCA1O0rURvrZgejA=s32-c-k-c0x00ffffff-no-rj","width":32,"height":32},{"url":"https://yt3.ggpht.com/ytc/AIdro_nG_pLAgEPHnWUEYGcnOnzJ08ED9uoCA1O0rURvrZgejA=s48-c-k-c0x00ffffff-no-rj","width":48,"height":48},{"url":"https://yt3.ggpht.com/ytc/AIdro_nG_pLAgEPHnWUEYGcnOnzJ08ED9uoCA1O0rURvrZgejA=s76-c-k-c0x00ffffff-no-rj","width":76,"height":76},{"url":"https://yt3.ggpht.com/ytc/AIdro_nG_pLAgEPHnWUEYGcnOnzJ08ED9uoCA1O0rURvrZgejA=s100-c-k-c0x00ffffff-no-rj","width":100,"height":100},{"url":"https://yt3.ggpht.com/ytc/AIdro_nG_pLAgEPHnWUEYGcnOnzJ08ED9uoCA1O0rURvrZgejA=s176-c-k-c0x00ffffff-no-rj","width":176,"height":176},{"url":"https://yt3.ggpht.com/ytc/AIdro_nG_pLAgEPHnWUEYGcnOnzJ08ED9uoCA1O0rURvrZgejA=s512-c-k-c0x00ffffff-no-rj","width":512,"height":512}],"subCountText":"7.09K","lengthSeconds":1509,"allowRatings":false,"rating":0,"isListed":true,"liveNow":false,"isPostLiveDvr":false,"isUpcoming":false,"dashUrl":"https://inv.nadeko.net/api/manifest/dash/id/b0tbxShxFws","adaptiveFormats":[{"init":"0-631","index":"632-2487","bitrate":"131664","url":"https://rr5---sn-uxgg5-njall.googlevideo.com/videoplayback?expire=1732947479&ei=t1lKZ8T7HcSa-LAP9tXTkAc&ip=186.105.135.2&id=o-AENVfEsZZWhYzdCbUPI-vImVvCghHteANDa15bobFGdu&itag=140&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&met=1732925879%2C&mh=jG&mm=31%2C29&mn=sn-uxgg5-njall%2Csn-uxgg5-njaed&ms=au%2Crdu&mv=m&mvi=5&pl=19&rms=au%2Cau&initcwndbps=2130000&bui=AQn3pFSF0H7g2gyAhdZtd7e04ICfNzC58h7omyEl18gcrwn8lV8EXydUYYfxS1H_M_jCBRn-fAwQfVkQ&spc=qtApAf0U6DX4dAZRvrtzuOGblFhz0Qj-B4SLDpT2qfrIZkp606b30-EpTD0g&vprv=1&svpuc=1&mime=audio%2Fmp4&ns=13kmSTCEkfIMEOYJ_A07a-IQ&rqh=1&gir=yes&clen=24407521&ratebypass=yes&dur=1508.089&lmt=1693560460480545&mt=1732925365&fvip=3&keepalive=yes&fexp=51326932%2C51335594&c=WEB&sefc=1&txp=5318224&n=SGlh7GDJQ7_Iew&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Cns%2Crqh%2Cgir%2Cclen%2Cratebypass%2Cdur%2Clmt&sig=AJfQdSswRAIgZ5s5fKS1rdpeTHYGBmQy92B4Mtg01ws312c1dBqGxyMCIBvr2U2RF12nr6FVaN5WI84RpcF1KdY_yTcNInaADrSP&lsparams=met%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=AGluJ3MwRQIgTZPXykTqCEsa4mW-2L6ba02UkKnBY6L06XqIvWt_oggCIQCzGplfkhGnF8VXYWXc_P_gFMTazE_XSlqx9tnSR9Z6xg%3D%3D&pot=MnRq9bywjIhAa2rNNl4PwaRveWDHtTfryA6TLKmTJalZzwcVWJlWpCM8BcrotpmQWa4JK6nxFZwMVsRVb9N2qwpKt6ZrRzk6jccaztfL9FDByAaSI_JV3_fqCO9gpNFZDaxEiugTg3nqyhlcF-NcuN-nh4z_EA%3D%3D","itag":"140","type":"audio/mp4; codecs=\"mp4a.40.2\"","clen":"24407521","lmt":"1693560460480545","projectionType":"RECTANGULAR","container":"m4a","encoding":"aac","audioQuality":"AUDIO_QUALITY_MEDIUM","audioSampleRate":44100,"audioChannels":2},{"init":"0-258","index":"259-2851","bitrate":"123603","url":"https://rr5---sn-uxgg5-njall.googlevideo.com/videoplayback?expire=1732947479&ei=t1lKZ8T7HcSa-LAP9tXTkAc&ip=186.105.135.2&id=o-AENVfEsZZWhYzdCbUPI-vImVvCghHteANDa15bobFGdu&itag=251&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&met=1732925879%2C&mh=jG&mm=31%2C29&mn=sn-uxgg5-njall%2Csn-uxgg5-njaed&ms=au%2Crdu&mv=m&mvi=5&pl=19&rms=au%2Cau&initcwndbps=2130000&bui=AQn3pFSF0H7g2gyAhdZtd7e04ICfNzC58h7omyEl18gcrwn8lV8EXydUYYfxS1H_M_jCBRn-fAwQfVkQ&spc=qtApAf0U6DX4dAZRvrtzuOGblFhz0Qj-B4SLDpT2qfrIZkp606b30-EpTD0g&vprv=1&svpuc=1&mime=audio%2Fwebm&ns=13kmSTCEkfIMEOYJ_A07a-IQ&rqh=1&gir=yes&clen=20825069&ratebypass=yes&dur=1508.061&lmt=1693560555185990&mt=1732925365&fvip=3&keepalive=yes&fexp=51326932%2C51335594&c=WEB&sefc=1&txp=5318224&n=SGlh7GDJQ7_Iew&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Cns%2Crqh%2Cgir%2Cclen%2Cratebypass%2Cdur%2Clmt&sig=AJfQdSswRQIgNEdgzQMQE6fsTpOPSbD-tXM6F3hEv4DVQqVgDDDA0P8CIQDlhNvTKl9idVkqNoc94VgbWYYij98HKNjJ8PrkC82UuA%3D%3D&lsparams=met%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=AGluJ3MwRQIgTZPXykTqCEsa4mW-2L6ba02UkKnBY6L06XqIvWt_oggCIQCzGplfkhGnF8VXYWXc_P_gFMTazE_XSlqx9tnSR9Z6xg%3D%3D&pot=MnRq9bywjIhAa2rNNl4PwaRveWDHtTfryA6TLKmTJalZzwcVWJlWpCM8BcrotpmQWa4JK6nxFZwMVsRVb9N2qwpKt6ZrRzk6jccaztfL9FDByAaSI_JV3_fqCO9gpNFZDaxEiugTg3nqyhlcF-NcuN-nh4z_EA%3D%3D","itag":"251","type":"audio/webm; codecs=\"opus\"","clen":"20825069","lmt":"1693560555185990","projectionType":"RECTANGULAR","container":"webm","encoding":"opus","audioQuality":"AUDIO_QUALITY_MEDIUM","audioSampleRate":48000,"audioChannels":2},{"init":"0-738","index":"739-4346","bitrate":"127152","url":"https://rr5---sn-uxgg5-njall.googlevideo.com/videoplayback?expire=1732947479&ei=t1lKZ8T7HcSa-LAP9tXTkAc&ip=186.105.135.2&id=o-AENVfEsZZWhYzdCbUPI-vImVvCghHteANDa15bobFGdu&itag=160&aitags=134%2C136%2C160%2C243%2C298%2C299&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&met=1732925879%2C&mh=jG&mm=31%2C29&mn=sn-uxgg5-njall%2Csn-uxgg5-njaed&ms=au%2Crdu&mv=m&mvi=5&pl=19&rms=au%2Cau&initcwndbps=2130000&bui=AQn3pFSF0H7g2gyAhdZtd7e04ICfNzC58h7omyEl18gcrwn8lV8EXydUYYfxS1H_M_jCBRn-fAwQfVkQ&spc=qtApAf0U6DX4dAZRvrtzuOGblFhz0Qj-B4SLDpT2qfrIZkp606b30-EpTD0g&vprv=1&svpuc=1&mime=video%2Fmp4&ns=13kmSTCEkfIMEOYJ_A07a-IQ&rqh=1&gir=yes&clen=15369990&ratebypass=yes&dur=1508.033&lmt=1693560498914579&mt=1732925365&fvip=3&keepalive=yes&fexp=51326932%2C51335594&c=WEB&sefc=1&txp=5319224&n=SGlh7GDJQ7_Iew&sparams=expire%2Cei%2Cip%2Cid%2Caitags%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Cns%2Crqh%2Cgir%2Cclen%2Cratebypass%2Cdur%2Clmt&sig=AJfQdSswRAIgFlL49Vh8x0eznG5oDYQ_F-FusJ5JbRwzPnG-Xdm64F4CIFvPttVRS2hyLKFfk8Kj_AmfaWmdms_5HtS0byT3vjwr&lsparams=met%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=AGluJ3MwRQIgTZPXykTqCEsa4mW-2L6ba02UkKnBY6L06XqIvWt_oggCIQCzGplfkhGnF8VXYWXc_P_gFMTazE_XSlqx9tnSR9Z6xg%3D%3D&pot=MnRq9bywjIhAa2rNNl4PwaRveWDHtTfryA6TLKmTJalZzwcVWJlWpCM8BcrotpmQWa4JK6nxFZwMVsRVb9N2qwpKt6ZrRzk6jccaztfL9FDByAaSI_JV3_fqCO9gpNFZDaxEiugTg3nqyhlcF-NcuN-nh4z_EA%3D%3D","itag":"160","type":"video/mp4; codecs=\"avc1.4d400c\"","clen":"15369990","lmt":"1693560498914579","projectionType":"RECTANGULAR","fps":30,"size":"256x144","resolution":"144p","qualityLabel":"144p","container":"mp4","encoding":"h264"},{"init":"0-740","index":"741-4348","bitrate":"623505","url":"https://rr5---sn-uxgg5-njall.googlevideo.com/videoplayback?expire=1732947479&ei=t1lKZ8T7HcSa-LAP9tXTkAc&ip=186.105.135.2&id=o-AENVfEsZZWhYzdCbUPI-vImVvCghHteANDa15bobFGdu&itag=134&aitags=134%2C136%2C160%2C243%2C298%2C299&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&met=1732925879%2C&mh=jG&mm=31%2C29&mn=sn-uxgg5-njall%2Csn-uxgg5-njaed&ms=au%2Crdu&mv=m&mvi=5&pl=19&rms=au%2Cau&initcwndbps=2130000&bui=AQn3pFSF0H7g2gyAhdZtd7e04ICfNzC58h7omyEl18gcrwn8lV8EXydUYYfxS1H_M_jCBRn-fAwQfVkQ&spc=qtApAf0U6DX4dAZRvrtzuOGblFhz0Qj-B4SLDpT2qfrIZkp606b30-EpTD0g&vprv=1&svpuc=1&mime=video%2Fmp4&ns=13kmSTCEkfIMEOYJ_A07a-IQ&rqh=1&gir=yes&clen=63748356&ratebypass=yes&dur=1508.033&lmt=1693560504492262&mt=1732925365&fvip=3&keepalive=yes&fexp=51326932%2C51335594&c=WEB&sefc=1&txp=5319224&n=SGlh7GDJQ7_Iew&sparams=expire%2Cei%2Cip%2Cid%2Caitags%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Cns%2Crqh%2Cgir%2Cclen%2Cratebypass%2Cdur%2Clmt&sig=AJfQdSswRgIhAOKKgKzVyYiDUYIWu4jvmk30elnqFp-FOwWcmNgTMSHLAiEA1gAvT8EYsuT9s--V8tjo6Ieex1iNXPzvPXyZ7sKdF2c%3D&lsparams=met%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=AGluJ3MwRQIgTZPXykTqCEsa4mW-2L6ba02UkKnBY6L06XqIvWt_oggCIQCzGplfkhGnF8VXYWXc_P_gFMTazE_XSlqx9tnSR9Z6xg%3D%3D&pot=MnRq9bywjIhAa2rNNl4PwaRveWDHtTfryA6TLKmTJalZzwcVWJlWpCM8BcrotpmQWa4JK6nxFZwMVsRVb9N2qwpKt6ZrRzk6jccaztfL9FDByAaSI_JV3_fqCO9gpNFZDaxEiugTg3nqyhlcF-NcuN-nh4z_EA%3D%3D","itag":"134","type":"video/mp4; codecs=\"avc1.4d401e\"","clen":"63748356","lmt":"1693560504492262","projectionType":"RECTANGULAR","fps":30,"size":"640x360","resolution":"360p","qualityLabel":"360p","container":"mp4","encoding":"h264"},{"init":"0-219","index":"220-5461","bitrate":"325874","url":"https://rr5---sn-uxgg5-njall.googlevideo.com/videoplayback?expire=1732947479&ei=t1lKZ8T7HcSa-LAP9tXTkAc&ip=186.105.135.2&id=o-AENVfEsZZWhYzdCbUPI-vImVvCghHteANDa15bobFGdu&itag=243&aitags=134%2C136%2C160%2C243%2C298%2C299&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&met=1732925879%2C&mh=jG&mm=31%2C29&mn=sn-uxgg5-njall%2Csn-uxgg5-njaed&ms=au%2Crdu&mv=m&mvi=5&pl=19&rms=au%2Cau&initcwndbps=2130000&bui=AQn3pFSF0H7g2gyAhdZtd7e04ICfNzC58h7omyEl18gcrwn8lV8EXydUYYfxS1H_M_jCBRn-fAwQfVkQ&spc=qtApAf0U6DX4dAZRvrtzuOGblFhz0Qj-B4SLDpT2qfrIZkp606b30-EpTD0g&vprv=1&svpuc=1&mime=video%2Fwebm&ns=13kmSTCEkfIMEOYJ_A07a-IQ&rqh=1&gir=yes&clen=46181568&ratebypass=yes&dur=1508.033&lmt=1693560469972855&mt=1732925365&fvip=3&keepalive=yes&fexp=51326932%2C51335594&c=WEB&sefc=1&txp=531F224&n=SGlh7GDJQ7_Iew&sparams=expire%2Cei%2Cip%2Cid%2Caitags%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Cns%2Crqh%2Cgir%2Cclen%2Cratebypass%2Cdur%2Clmt&sig=AJfQdSswRAIgAyeM6BlHLeZAtTsOdrJt2ymt6v40oSmvDYGAxZ45N4oCIGe99IUPsvF9fCgwWyOAr6VF2RokedqaSMxd-8pN9Ats&lsparams=met%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=AGluJ3MwRQIgTZPXykTqCEsa4mW-2L6ba02UkKnBY6L06XqIvWt_oggCIQCzGplfkhGnF8VXYWXc_P_gFMTazE_XSlqx9tnSR9Z6xg%3D%3D&pot=MnRq9bywjIhAa2rNNl4PwaRveWDHtTfryA6TLKmTJalZzwcVWJlWpCM8BcrotpmQWa4JK6nxFZwMVsRVb9N2qwpKt6ZrRzk6jccaztfL9FDByAaSI_JV3_fqCO9gpNFZDaxEiugTg3nqyhlcF-NcuN-nh4z_EA%3D%3D","itag":"243","type":"video/webm; codecs=\"vp9\"","clen":"46181568","lmt":"1693560469972855","projectionType":"RECTANGULAR","fps":30,"size":"640x360","resolution":"360p","qualityLabel":"360p","container":"webm","encoding":"vp9","colorInfo":{"primaries":"COLOR_PRIMARIES_BT709","transferCharacteristics":"COLOR_TRANSFER_CHARACTERISTICS_BT709","matrixCoefficients":"COLOR_MATRIX_COEFFICIENTS_BT709"}},{"init":"0-739","index":"740-4347","bitrate":"2148204","url":"https://rr5---sn-uxgg5-njall.googlevideo.com/videoplayback?expire=1732947479&ei=t1lKZ8T7HcSa-LAP9tXTkAc&ip=186.105.135.2&id=o-AENVfEsZZWhYzdCbUPI-vImVvCghHteANDa15bobFGdu&itag=136&aitags=134%2C136%2C160%2C243%2C298%2C299&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&met=1732925879%2C&mh=jG&mm=31%2C29&mn=sn-uxgg5-njall%2Csn-uxgg5-njaed&ms=au%2Crdu&mv=m&mvi=5&pl=19&rms=au%2Cau&initcwndbps=2130000&bui=AQn3pFSF0H7g2gyAhdZtd7e04ICfNzC58h7omyEl18gcrwn8lV8EXydUYYfxS1H_M_jCBRn-fAwQfVkQ&spc=qtApAf0U6DX4dAZRvrtzuOGblFhz0Qj-B4SLDpT2qfrIZkp606b30-EpTD0g&vprv=1&svpuc=1&mime=video%2Fmp4&ns=13kmSTCEkfIMEOYJ_A07a-IQ&rqh=1&gir=yes&clen=227662449&ratebypass=yes&dur=1508.033&lmt=1693560453405552&mt=1732925365&fvip=3&keepalive=yes&fexp=51326932%2C51335594&c=WEB&sefc=1&txp=5319224&n=SGlh7GDJQ7_Iew&sparams=expire%2Cei%2Cip%2Cid%2Caitags%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Cns%2Crqh%2Cgir%2Cclen%2Cratebypass%2Cdur%2Clmt&sig=AJfQdSswRAIgWjPxe3KnxiHBpy15GKVjRub-RSC6Tte8djJy_ZBWz9YCIEBIcWNRbmeya-LW6JpgpNP5F9oEhQqLCDlwx-sI4-_d&lsparams=met%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=AGluJ3MwRQIgTZPXykTqCEsa4mW-2L6ba02UkKnBY6L06XqIvWt_oggCIQCzGplfkhGnF8VXYWXc_P_gFMTazE_XSlqx9tnSR9Z6xg%3D%3D&pot=MnRq9bywjIhAa2rNNl4PwaRveWDHtTfryA6TLKmTJalZzwcVWJlWpCM8BcrotpmQWa4JK6nxFZwMVsRVb9N2qwpKt6ZrRzk6jccaztfL9FDByAaSI_JV3_fqCO9gpNFZDaxEiugTg3nqyhlcF-NcuN-nh4z_EA%3D%3D","itag":"136","type":"video/mp4; codecs=\"avc1.64001f\"","clen":"227662449","lmt":"1693560453405552","projectionType":"RECTANGULAR","fps":30,"size":"1280x720","resolution":"720p","qualityLabel":"720p","container":"mp4","encoding":"h264"},{"init":"0-739","index":"740-4347","bitrate":"4035002","url":"https://rr5---sn-uxgg5-njall.googlevideo.com/videoplayback?expire=1732947479&ei=t1lKZ8T7HcSa-LAP9tXTkAc&ip=186.105.135.2&id=o-AENVfEsZZWhYzdCbUPI-vImVvCghHteANDa15bobFGdu&itag=298&aitags=134%2C136%2C160%2C243%2C298%2C299&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&met=1732925879%2C&mh=jG&mm=31%2C29&mn=sn-uxgg5-njall%2Csn-uxgg5-njaed&ms=au%2Crdu&mv=m&mvi=5&pl=19&rms=au%2Cau&initcwndbps=2130000&bui=AQn3pFSF0H7g2gyAhdZtd7e04ICfNzC58h7omyEl18gcrwn8lV8EXydUYYfxS1H_M_jCBRn-fAwQfVkQ&spc=qtApAf0U6DX4dAZRvrtzuOGblFhz0Qj-B4SLDpT2qfrIZkp606b30-EpTD0g&vprv=1&svpuc=1&mime=video%2Fmp4&ns=13kmSTCEkfIMEOYJ_A07a-IQ&rqh=1&gir=yes&clen=329893030&ratebypass=yes&dur=1508.033&lmt=1693560482617647&mt=1732925365&fvip=3&keepalive=yes&fexp=51326932%2C51335594&c=WEB&sefc=1&txp=5319224&n=SGlh7GDJQ7_Iew&sparams=expire%2Cei%2Cip%2Cid%2Caitags%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Cns%2Crqh%2Cgir%2Cclen%2Cratebypass%2Cdur%2Clmt&sig=AJfQdSswRQIhANVk_dM2e1KXDDGkYUtbmy4EQ7Ome4uIyYCVehe0LEt1AiATHRXNjMtDjjRmnoOS1D-GFHfmVKe-HMT1-iavKQ-YZg%3D%3D&lsparams=met%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=AGluJ3MwRQIgTZPXykTqCEsa4mW-2L6ba02UkKnBY6L06XqIvWt_oggCIQCzGplfkhGnF8VXYWXc_P_gFMTazE_XSlqx9tnSR9Z6xg%3D%3D&pot=MnRq9bywjIhAa2rNNl4PwaRveWDHtTfryA6TLKmTJalZzwcVWJlWpCM8BcrotpmQWa4JK6nxFZwMVsRVb9N2qwpKt6ZrRzk6jccaztfL9FDByAaSI_JV3_fqCO9gpNFZDaxEiugTg3nqyhlcF-NcuN-nh4z_EA%3D%3D","itag":"298","type":"video/mp4; codecs=\"avc1.640020\"","clen":"329893030","lmt":"1693560482617647","projectionType":"RECTANGULAR","fps":60,"size":"1280x720","resolution":"720p","qualityLabel":"720p60","container":"mp4","encoding":"h264"},{"init":"0-741","index":"742-4349","bitrate":"6394939","url":"https://rr5---sn-uxgg5-njall.googlevideo.com/videoplayback?expire=1732947479&ei=t1lKZ8T7HcSa-LAP9tXTkAc&ip=186.105.135.2&id=o-AENVfEsZZWhYzdCbUPI-vImVvCghHteANDa15bobFGdu&itag=299&aitags=134%2C136%2C160%2C243%2C298%2C299&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&met=1732925879%2C&mh=jG&mm=31%2C29&mn=sn-uxgg5-njall%2Csn-uxgg5-njaed&ms=au%2Crdu&mv=m&mvi=5&pl=19&rms=au%2Cau&initcwndbps=2130000&bui=AQn3pFSF0H7g2gyAhdZtd7e04ICfNzC58h7omyEl18gcrwn8lV8EXydUYYfxS1H_M_jCBRn-fAwQfVkQ&spc=qtApAf0U6DX4dAZRvrtzuOGblFhz0Qj-B4SLDpT2qfrIZkp606b30-EpTD0g&vprv=1&svpuc=1&mime=video%2Fmp4&ns=13kmSTCEkfIMEOYJ_A07a-IQ&rqh=1&gir=yes&clen=616540478&ratebypass=yes&dur=1508.033&lmt=1693560752008391&mt=1732925365&fvip=3&keepalive=yes&fexp=51326932%2C51335594&c=WEB&sefc=1&txp=5319224&n=SGlh7GDJQ7_Iew&sparams=expire%2Cei%2Cip%2Cid%2Caitags%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Cns%2Crqh%2Cgir%2Cclen%2Cratebypass%2Cdur%2Clmt&sig=AJfQdSswRQIgM4qBRjfV-JXUx_oTmwoVkG-hgzVkOyQ66LI-A_3_woUCIQD3YFo4s750KShK_3ldOtBnwg0YsIcb-Zvf9E3exyq7Dw%3D%3D&lsparams=met%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=AGluJ3MwRQIgTZPXykTqCEsa4mW-2L6ba02UkKnBY6L06XqIvWt_oggCIQCzGplfkhGnF8VXYWXc_P_gFMTazE_XSlqx9tnSR9Z6xg%3D%3D&pot=MnRq9bywjIhAa2rNNl4PwaRveWDHtTfryA6TLKmTJalZzwcVWJlWpCM8BcrotpmQWa4JK6nxFZwMVsRVb9N2qwpKt6ZrRzk6jccaztfL9FDByAaSI_JV3_fqCO9gpNFZDaxEiugTg3nqyhlcF-NcuN-nh4z_EA%3D%3D","itag":"299","type":"video/mp4; codecs=\"avc1.64002a\"","clen":"616540478","lmt":"1693560752008391","projectionType":"RECTANGULAR","fps":60,"size":"1920x1080","resolution":"1080p","qualityLabel":"1080p60","container":"mp4","encoding":"h264"}],"formatStreams":[{"url":"https://rr5---sn-uxgg5-njall.googlevideo.com/videoplayback?expire=1732947479&ei=t1lKZ8T7HcSa-LAP9tXTkAc&ip=186.105.135.2&id=o-AENVfEsZZWhYzdCbUPI-vImVvCghHteANDa15bobFGdu&itag=18&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&met=1732925879%2C&mh=jG&mm=31%2C29&mn=sn-uxgg5-njall%2Csn-uxgg5-njaed&ms=au%2Crdu&mv=m&mvi=5&pl=19&rms=au%2Cau&initcwndbps=2130000&bui=AQn3pFSW1NyiyFgIKvRz5KqHk5HNzlhT7ptEzV_zNzVSCNpQJw3ajltXaDtqTDa60yeT2U7SrSTk7H8q&spc=qtApAf0X6DX4dAZRvrtzuOGblFhy0Qj-B4SLDpT2qfrIZkp606b30-EpTA0ltuE&vprv=1&svpuc=1&mime=video%2Fmp4&ns=6f4vxadwK1L9EFjYyuGJlgsQ&rqh=1&cnr=14&ratebypass=yes&dur=1508.089&lmt=1698426319995100&mt=1732925365&fvip=3&fexp=51326932%2C51335594&c=WEB&sefc=1&txp=5318224&n=W09BHQAFNN6iEw&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Cns%2Crqh%2Ccnr%2Cratebypass%2Cdur%2Clmt&sig=AJfQdSswRQIgFqOpl9ebUrLg4Xcjc0vd9KCvQEIK1zSuLU21zK2SgdUCIQCz1qW1tX5ciiPTtlq_KVlxZ_0huipjQvqogLmSZyd3bQ%3D%3D&lsparams=met%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=AGluJ3MwRQIgTZPXykTqCEsa4mW-2L6ba02UkKnBY6L06XqIvWt_oggCIQCzGplfkhGnF8VXYWXc_P_gFMTazE_XSlqx9tnSR9Z6xg%3D%3D&pot=MnRq9bywjIhAa2rNNl4PwaRveWDHtTfryA6TLKmTJalZzwcVWJlWpCM8BcrotpmQWa4JK6nxFZwMVsRVb9N2qwpKt6ZrRzk6jccaztfL9FDByAaSI_JV3_fqCO9gpNFZDaxEiugTg3nqyhlcF-NcuN-nh4z_EA%3D%3D","itag":"18","type":"video/mp4; codecs=\"avc1.42001E, mp4a.40.2\"","quality":"medium","bitrate":"466305","fps":30,"size":"640x360","resolution":"360p","qualityLabel":"360p","container":"mp4","encoding":"h264"}],"captions":[{"label":"Japanese (auto-generated)","language_code":"ja","url":"/api/v1/captions/b0tbxShxFws?label=Japanese+%28auto-generated%29"}],"recommendedVideos":[{"videoId":"47d__x41_Gk","title":"【英検新形式】１級・準１級・２級　要約問題を解くための３ STEPS","videoThumbnails":[{"quality":"maxres","url":"https://inv.nadeko.net/vi/47d__x41_Gk/maxres.jpg","width":1280,"height":720},{"quality":"maxresdefault","url":"https://inv.nadeko.net/vi/47d__x41_Gk/maxresdefault.jpg","width":1280,"height":720},{"quality":"sddefault","url":"https://inv.nadeko.net/vi/47d__x41_Gk/sddefault.jpg","width":640,"height":480},{"quality":"high","url":"https://inv.nadeko.net/vi/47d__x41_Gk/hqdefault.jpg","width":480,"height":360},{"quality":"medium","url":"https://inv.nadeko.net/vi/47d__x41_Gk/mqdefault.jpg","width":320,"height":180},{"quality":"default","url":"https://inv.nadeko.net/vi/47d__x41_Gk/default.jpg","width":120,"height":90},{"quality":"start","url":"https://inv.nadeko.net/vi/47d__x41_Gk/1.jpg","width":120,"height":90},{"quality":"middle","url":"https://inv.nadeko.net/vi/47d__x41_Gk/2.jpg","width":120,"height":90},{"quality":"end","url":"https://inv.nadeko.net/vi/47d__x41_Gk/3.jpg","width":120,"height":90}],"author":"英語ファイル / eigophile","authorUrl":"/channel/UCbGSTOIeDaP-t3D5SerWpWg","authorId":"UCbGSTOIeDaP-t3D5SerWpWg","authorVerified":false,"lengthSeconds":814,"viewCountText":"72K","viewCount":72040},{"videoId":"X2Vrik4oQfI","title":"【英検2024リニューアル解説動画】英検準1級の変更点と勉強法（安河内哲也先生）","videoThumbnails":[{"quality":"maxres","url":"https://inv.nadeko.net/vi/X2Vrik4oQfI/maxres.jpg","width":1280,"height":720},{"quality":"maxresdefault","url":"https://inv.nadeko.net/vi/X2Vrik4oQfI/maxresdefault.jpg","width":1280,"height":720},{"quality":"sddefault","url":"https://inv.nadeko.net/vi/X2Vrik4oQfI/sddefault.jpg","width":640,"height":480},{"quality":"high","url":"https://inv.nadeko.net/vi/X2Vrik4oQfI/hqdefault.jpg","width":480,"height":360},{"quality":"medium","url":"https://inv.nadeko.net/vi/X2Vrik4oQfI/mqdefault.jpg","width":320,"height":180},{"quality":"default","url":"https://inv.nadeko.net/vi/X2Vrik4oQfI/default.jpg","width":120,"height":90},{"quality":"start","url":"https://inv.nadeko.net/vi/X2Vrik4oQfI/1.jpg","width":120,"height":90},{"quality":"middle","url":"https://inv.nadeko.net/vi/X2Vrik4oQfI/2.jpg","width":120,"height":90},{"quality":"end","url":"https://inv.nadeko.net/vi/X2Vrik4oQfI/3.jpg","width":120,"height":90}],"author":"Eiken Foundation of Japan","authorUrl":"/channel/UCYLj-_GA6hHV0fd6A9pMGow","authorId":"UCYLj-_GA6hHV0fd6A9pMGow","authorVerified":false,"lengthSeconds":993,"viewCountText":"50K","viewCount":50225},{"videoId":"1MHbRfaE_tg","title":"今すぐ使える英作文神フレーズ集！この通りに書けばライティングで満点取れます","videoThumbnails":[{"quality":"maxres","url":"https://inv.nadeko.net/vi/1MHbRfaE_tg/maxres.jpg","width":1280,"height":720},{"quality":"maxresdefault","url":"https://inv.nadeko.net/vi/1MHbRfaE_tg/maxresdefault.jpg","width":1280,"height":720},{"quality":"sddefault","url":"https://inv.nadeko.net/vi/1MHbRfaE_tg/sddefault.jpg","width":640,"height":480},{"quality":"high","url":"https://inv.nadeko.net/vi/1MHbRfaE_tg/hqdefault.jpg","width":480,"height":360},{"quality":"medium","url":"https://inv.nadeko.net/vi/1MHbRfaE_tg/mqdefault.jpg","width":320,"height":180},{"quality":"default","url":"https://inv.nadeko.net/vi/1MHbRfaE_tg/default.jpg","width":120,"height":90},{"quality":"start","url":"https://inv.nadeko.net/vi/1MHbRfaE_tg/1.jpg","width":120,"height":90},{"quality":"middle","url":"https://inv.nadeko.net/vi/1MHbRfaE_tg/2.jpg","width":120,"height":90},{"quality":"end","url":"https://inv.nadeko.net/vi/1MHbRfaE_tg/3.jpg","width":120,"height":90}],"author":"さむらい英語塾 / 英検対策チャンネル","authorUrl":"/channel/UCv9OTTw1BXZ8S8vzszn__pA","authorId":"UCv9OTTw1BXZ8S8vzszn__pA","authorVerified":false,"lengthSeconds":485,"viewCountText":"593K","viewCount":593814},{"videoId":"SWfNNlNOQCY","title":"英検2級の攻略法【勉強法・時間配分・戦略】","videoThumbnails":[{"quality":"maxres","url":"https://inv.nadeko.net/vi/SWfNNlNOQCY/maxres.jpg","width":1280,"height":720},{"quality":"maxresdefault","url":"https://inv.nadeko.net/vi/SWfNNlNOQCY/maxresdefault.jpg","width":1280,"height":720},{"quality":"sddefault","url":"https://inv.nadeko.net/vi/SWfNNlNOQCY/sddefault.jpg","width":640,"height":480},{"quality":"high","url":"https://inv.nadeko.net/vi/SWfNNlNOQCY/hqdefault.jpg","width":480,"height":360},{"quality":"medium","url":"https://inv.nadeko.net/vi/SWfNNlNOQCY/mqdefault.jpg","width":320,"height":180},{"quality":"default","url":"https://inv.nadeko.net/vi/SWfNNlNOQCY/default.jpg","width":120,"height":90},{"quality":"start","url":"https://inv.nadeko.net/vi/SWfNNlNOQCY/1.jpg","width":120,"height":90},{"quality":"middle","url":"https://inv.nadeko.net/vi/SWfNNlNOQCY/2.jpg","width":120,"height":90},{"quality":"end","url":"https://inv.nadeko.net/vi/SWfNNlNOQCY/3.jpg","width":120,"height":90}],"author":"Morite2 English Channel","authorUrl":"/channel/UC_U7pKOVK-0hGr7bDmy2mng","authorId":"UC_U7pKOVK-0hGr7bDmy2mng","authorVerified":true,"lengthSeconds":640,"viewCountText":"161K","viewCount":161024},{"videoId":"SaQxWXgIEXA","title":"【英語リスニング勉強法】正しい聞き流し法でリスニングが驚くほど上達！英検2級リスニング問題で実践練習。ベテラン英会話講師がお教えします","videoThumbnails":[{"quality":"maxres","url":"https://inv.nadeko.net/vi/SaQxWXgIEXA/maxres.jpg","width":1280,"height":720},{"quality":"maxresdefault","url":"https://inv.nadeko.net/vi/SaQxWXgIEXA/maxresdefault.jpg","width":1280,"height":720},{"quality":"sddefault","url":"https://inv.nadeko.net/vi/SaQxWXgIEXA/sddefault.jpg","width":640,"height":480},{"quality":"high","url":"https://inv.nadeko.net/vi/SaQxWXgIEXA/hqdefault.jpg","width":480,"height":360},{"quality":"medium","url":"https://inv.nadeko.net/vi/SaQxWXgIEXA/mqdefault.jpg","width":320,"height":180},{"quality":"default","url":"https://inv.nadeko.net/vi/SaQxWXgIEXA/default.jpg","width":120,"height":90},{"quality":"start","url":"https://inv.nadeko.net/vi/SaQxWXgIEXA/1.jpg","width":120,"height":90},{"quality":"middle","url":"https://inv.nadeko.net/vi/SaQxWXgIEXA/2.jpg","width":120,"height":90},{"quality":"end","url":"https://inv.nadeko.net/vi/SaQxWXgIEXA/3.jpg","width":120,"height":90}],"author":"オーチャード・イングリッシュ・アカデミー","authorUrl":"/channel/UCnlKuH07keQrJmVDtwk_wWA","authorId":"UCnlKuH07keQrJmVDtwk_wWA","authorVerified":false,"lengthSeconds":823,"viewCountText":"572","viewCount":572},{"videoId":"51M404panMA","title":"【英検準１級】ライティング満点が使っていたテンプレートを公開！","videoThumbnails":[{"quality":"maxres","url":"https://inv.nadeko.net/vi/51M404panMA/maxres.jpg","width":1280,"height":720},{"quality":"maxresdefault","url":"https://inv.nadeko.net/vi/51M404panMA/maxresdefault.jpg","width":1280,"height":720},{"quality":"sddefault","url":"https://inv.nadeko.net/vi/51M404panMA/sddefault.jpg","width":640,"height":480},{"quality":"high","url":"https://inv.nadeko.net/vi/51M404panMA/hqdefault.jpg","width":480,"height":360},{"quality":"medium","url":"https://inv.nadeko.net/vi/51M404panMA/mqdefault.jpg","width":320,"height":180},{"quality":"default","url":"https://inv.nadeko.net/vi/51M404panMA/default.jpg","width":120,"height":90},{"quality":"start","url":"https://inv.nadeko.net/vi/51M404panMA/1.jpg","width":120,"height":90},{"quality":"middle","url":"https://inv.nadeko.net/vi/51M404panMA/2.jpg","width":120,"height":90},{"quality":"end","url":"https://inv.nadeko.net/vi/51M404panMA/3.jpg","width":120,"height":90}],"author":"仮面浪人","authorUrl":"/channel/UCm7yyyKGvuzA8GQddR6e1Bg","authorId":"UCm7yyyKGvuzA8GQddR6e1Bg","authorVerified":false,"lengthSeconds":881,"viewCountText":"100K","viewCount":100348},{"videoId":"mNOvfFknKI0","title":"How Make Confidence In Speaking || Improve Your English Skills || Listen And Practice||Graded Reader","videoThumbnails":[{"quality":"maxres","url":"https://inv.nadeko.net/vi/mNOvfFknKI0/maxres.jpg","width":1280,"height":720},{"quality":"maxresdefault","url":"https://inv.nadeko.net/vi/mNOvfFknKI0/maxresdefault.jpg","width":1280,"height":720},{"quality":"sddefault","url":"https://inv.nadeko.net/vi/mNOvfFknKI0/sddefault.jpg","width":640,"height":480},{"quality":"high","url":"https://inv.nadeko.net/vi/mNOvfFknKI0/hqdefault.jpg","width":480,"height":360},{"quality":"medium","url":"https://inv.nadeko.net/vi/mNOvfFknKI0/mqdefault.jpg","width":320,"height":180},{"quality":"default","url":"https://inv.nadeko.net/vi/mNOvfFknKI0/default.jpg","width":120,"height":90},{"quality":"start","url":"https://inv.nadeko.net/vi/mNOvfFknKI0/1.jpg","width":120,"height":90},{"quality":"middle","url":"https://inv.nadeko.net/vi/mNOvfFknKI0/2.jpg","width":120,"height":90},{"quality":"end","url":"https://inv.nadeko.net/vi/mNOvfFknKI0/3.jpg","width":120,"height":90}],"author":"Learn English With Listening","authorUrl":"/channel/UC5aEw-wDITjH_KGceWLdMgA","authorId":"UC5aEw-wDITjH_KGceWLdMgA","authorVerified":false,"lengthSeconds":3673,"viewCountText":"949","viewCount":949},{"videoId":"gXs7Qj2aPVI","title":"【英検準1級】早稲田受験のために取った話するよ！","videoThumbnails":[{"quality":"maxres","url":"https://inv.nadeko.net/vi/gXs7Qj2aPVI/maxres.jpg","width":1280,"height":720},{"quality":"maxresdefault","url":"https://inv.nadeko.net/vi/gXs7Qj2aPVI/maxresdefault.jpg","width":1280,"height":720},{"quality":"sddefault","url":"https://inv.nadeko.net/vi/gXs7Qj2aPVI/sddefault.jpg","width":640,"height":480},{"quality":"high","url":"https://inv.nadeko.net/vi/gXs7Qj2aPVI/hqdefault.jpg","width":480,"height":360},{"quality":"medium","url":"https://inv.nadeko.net/vi/gXs7Qj2aPVI/mqdefault.jpg","width":320,"height":180},{"quality":"default","url":"https://inv.nadeko.net/vi/gXs7Qj2aPVI/default.jpg","width":120,"height":90},{"quality":"start","url":"https://inv.nadeko.net/vi/gXs7Qj2aPVI/1.jpg","width":120,"height":90},{"quality":"middle","url":"https://inv.nadeko.net/vi/gXs7Qj2aPVI/2.jpg","width":120,"height":90},{"quality":"end","url":"https://inv.nadeko.net/vi/gXs7Qj2aPVI/3.jpg","width":120,"height":90}],"author":"Kiyopi","authorUrl":"/channel/UCaRXpz23pytqbKi03sHnSRw","authorId":"UCaRXpz23pytqbKi03sHnSRw","authorVerified":false,"lengthSeconds":575,"viewCountText":"4.7K","viewCount":4716},{"videoId":"z5noc4wbr0A","title":"【3分でわかる！英検２級面接講座#1】問1パッセージ問題完全攻略","videoThumbnails":[{"quality":"maxres","url":"https://inv.nadeko.net/vi/z5noc4wbr0A/maxres.jpg","width":1280,"height":720},{"quality":"maxresdefault","url":"https://inv.nadeko.net/vi/z5noc4wbr0A/maxresdefault.jpg","width":1280,"height":720},{"quality":"sddefault","url":"https://inv.nadeko.net/vi/z5noc4wbr0A/sddefault.jpg","width":640,"height":480},{"quality":"high","url":"https://inv.nadeko.net/vi/z5noc4wbr0A/hqdefault.jpg","width":480,"height":360},{"quality":"medium","url":"https://inv.nadeko.net/vi/z5noc4wbr0A/mqdefault.jpg","width":320,"height":180},{"quality":"default","url":"https://inv.nadeko.net/vi/z5noc4wbr0A/default.jpg","width":120,"height":90},{"quality":"start","url":"https://inv.nadeko.net/vi/z5noc4wbr0A/1.jpg","width":120,"height":90},{"quality":"middle","url":"https://inv.nadeko.net/vi/z5noc4wbr0A/2.jpg","width":120,"height":90},{"quality":"end","url":"https://inv.nadeko.net/vi/z5noc4wbr0A/3.jpg","width":120,"height":90}],"author":"My Room英語学習デザイン研究所","authorUrl":"/channel/UCv4brhOjotzEfcOTf3SCP6w","authorId":"UCv4brhOjotzEfcOTf3SCP6w","authorVerified":false,"lengthSeconds":207,"viewCountText":"7.9K","viewCount":7966},{"videoId":"Wcl7mX1AgCo","title":"3度目の英検合格発表 writing大事故意味がわからん","videoThumbnails":[{"quality":"maxres","url":"https://inv.nadeko.net/vi/Wcl7mX1AgCo/maxres.jpg","width":1280,"height":720},{"quality":"maxresdefault","url":"https://inv.nadeko.net/vi/Wcl7mX1AgCo/maxresdefault.jpg","width":1280,"height":720},{"quality":"sddefault","url":"https://inv.nadeko.net/vi/Wcl7mX1AgCo/sddefault.jpg","width":640,"height":480},{"quality":"high","url":"https://inv.nadeko.net/vi/Wcl7mX1AgCo/hqdefault.jpg","width":480,"height":360},{"quality":"medium","url":"https://inv.nadeko.net/vi/Wcl7mX1AgCo/mqdefault.jpg","width":320,"height":180},{"quality":"default","url":"https://inv.nadeko.net/vi/Wcl7mX1AgCo/default.jpg","width":120,"height":90},{"quality":"start","url":"https://inv.nadeko.net/vi/Wcl7mX1AgCo/1.jpg","width":120,"height":90},{"quality":"middle","url":"https://inv.nadeko.net/vi/Wcl7mX1AgCo/2.jpg","width":120,"height":90},{"quality":"end","url":"https://inv.nadeko.net/vi/Wcl7mX1AgCo/3.jpg","width":120,"height":90}],"author":"いっちー [英語力0からUSCPAへ]","authorUrl":"/channel/UCbkGpjCz9hhRJ6gu_NuXRBw","authorId":"UCbkGpjCz9hhRJ6gu_NuXRBw","authorVerified":false,"lengthSeconds":583,"viewCountText":"29K","viewCount":29408},{"videoId":"lYTD7dV163c","title":"【英検準1級】1次結果","videoThumbnails":[{"quality":"maxres","url":"https://inv.nadeko.net/vi/lYTD7dV163c/maxres.jpg","width":1280,"height":720},{"quality":"maxresdefault","url":"https://inv.nadeko.net/vi/lYTD7dV163c/maxresdefault.jpg","width":1280,"height":720},{"quality":"sddefault","url":"https://inv.nadeko.net/vi/lYTD7dV163c/sddefault.jpg","width":640,"height":480},{"quality":"high","url":"https://inv.nadeko.net/vi/lYTD7dV163c/hqdefault.jpg","width":480,"height":360},{"quality":"medium","url":"https://inv.nadeko.net/vi/lYTD7dV163c/mqdefault.jpg","width":320,"height":180},{"quality":"default","url":"https://inv.nadeko.net/vi/lYTD7dV163c/default.jpg","width":120,"height":90},{"quality":"start","url":"https://inv.nadeko.net/vi/lYTD7dV163c/1.jpg","width":120,"height":90},{"quality":"middle","url":"https://inv.nadeko.net/vi/lYTD7dV163c/2.jpg","width":120,"height":90},{"quality":"end","url":"https://inv.nadeko.net/vi/lYTD7dV163c/3.jpg","width":120,"height":90}],"author":"浪人忍(ろうにんにん)","authorUrl":"/channel/UCWea__O1aewN6ttvXWPVnhA","authorId":"UCWea__O1aewN6ttvXWPVnhA","authorVerified":false,"lengthSeconds":644,"viewCountText":"7.3K","viewCount":7362},{"videoId":"28fkInVJCK0","title":"Why You Can Understand But Can't Speak | Graded Reader | Learn English Speaking","videoThumbnails":[{"quality":"maxres","url":"https://inv.nadeko.net/vi/28fkInVJCK0/maxres.jpg","width":1280,"height":720},{"quality":"maxresdefault","url":"https://inv.nadeko.net/vi/28fkInVJCK0/maxresdefault.jpg","width":1280,"height":720},{"quality":"sddefault","url":"https://inv.nadeko.net/vi/28fkInVJCK0/sddefault.jpg","width":640,"height":480},{"quality":"high","url":"https://inv.nadeko.net/vi/28fkInVJCK0/hqdefault.jpg","width":480,"height":360},{"quality":"medium","url":"https://inv.nadeko.net/vi/28fkInVJCK0/mqdefault.jpg","width":320,"height":180},{"quality":"default","url":"https://inv.nadeko.net/vi/28fkInVJCK0/default.jpg","width":120,"height":90},{"quality":"start","url":"https://inv.nadeko.net/vi/28fkInVJCK0/1.jpg","width":120,"height":90},{"quality":"middle","url":"https://inv.nadeko.net/vi/28fkInVJCK0/2.jpg","width":120,"height":90},{"quality":"end","url":"https://inv.nadeko.net/vi/28fkInVJCK0/3.jpg","width":120,"height":90}],"author":"Simple Spoken English Star","authorUrl":"/channel/UCrj_8gDeBDmJG73K4b81bNQ","authorId":"UCrj_8gDeBDmJG73K4b81bNQ","authorVerified":false,"lengthSeconds":1067,"viewCountText":"219","viewCount":219},{"videoId":"xZLFQPjs_bU","title":"英検一級合格発表","videoThumbnails":[{"quality":"maxres","url":"https://inv.nadeko.net/vi/xZLFQPjs_bU/maxres.jpg","width":1280,"height":720},{"quality":"maxresdefault","url":"https://inv.nadeko.net/vi/xZLFQPjs_bU/maxresdefault.jpg","width":1280,"height":720},{"quality":"sddefault","url":"https://inv.nadeko.net/vi/xZLFQPjs_bU/sddefault.jpg","width":640,"height":480},{"quality":"high","url":"https://inv.nadeko.net/vi/xZLFQPjs_bU/hqdefault.jpg","width":480,"height":360},{"quality":"medium","url":"https://inv.nadeko.net/vi/xZLFQPjs_bU/mqdefault.jpg","width":320,"height":180},{"quality":"default","url":"https://inv.nadeko.net/vi/xZLFQPjs_bU/default.jpg","width":120,"height":90},{"quality":"start","url":"https://inv.nadeko.net/vi/xZLFQPjs_bU/1.jpg","width":120,"height":90},{"quality":"middle","url":"https://inv.nadeko.net/vi/xZLFQPjs_bU/2.jpg","width":120,"height":90},{"quality":"end","url":"https://inv.nadeko.net/vi/xZLFQPjs_bU/3.jpg","width":120,"height":90}],"author":"みかん@勉強Youtuber","authorUrl":"/channel/UCzh9r_Rr3ZnS5EDgIQqz92g","authorId":"UCzh9r_Rr3ZnS5EDgIQqz92g","authorVerified":false,"lengthSeconds":890,"viewCountText":"1.2K","viewCount":1263},{"videoId":"3GOmJyTfRjg","title":"I Regret Marrying Him ✅ Learn English Through Stories ✅","videoThumbnails":[{"quality":"maxres","url":"https://inv.nadeko.net/vi/3GOmJyTfRjg/maxres.jpg","width":1280,"height":720},{"quality":"maxresdefault","url":"https://inv.nadeko.net/vi/3GOmJyTfRjg/maxresdefault.jpg","width":1280,"height":720},{"quality":"sddefault","url":"https://inv.nadeko.net/vi/3GOmJyTfRjg/sddefault.jpg","width":640,"height":480},{"quality":"high","url":"https://inv.nadeko.net/vi/3GOmJyTfRjg/hqdefault.jpg","width":480,"height":360},{"quality":"medium","url":"https://inv.nadeko.net/vi/3GOmJyTfRjg/mqdefault.jpg","width":320,"height":180},{"quality":"default","url":"https://inv.nadeko.net/vi/3GOmJyTfRjg/default.jpg","width":120,"height":90},{"quality":"start","url":"https://inv.nadeko.net/vi/3GOmJyTfRjg/1.jpg","width":120,"height":90},{"quality":"middle","url":"https://inv.nadeko.net/vi/3GOmJyTfRjg/2.jpg","width":120,"height":90},{"quality":"end","url":"https://inv.nadeko.net/vi/3GOmJyTfRjg/3.jpg","width":120,"height":90}],"author":"English Stories with Allicia 2","authorUrl":"/channel/UCTp1FxUT8Yo_o0n52EJ-ndQ","authorId":"UCTp1FxUT8Yo_o0n52EJ-ndQ","authorVerified":false,"lengthSeconds":581,"viewCountText":"15K","viewCount":15898},{"videoId":"mwA4XA0GSIY","title":"【英検準1級 】試験5分前でも覚えられる　超簡単テンプレ スピーキング／二次試験対策　ナレーション","videoThumbnails":[{"quality":"maxres","url":"https://inv.nadeko.net/vi/mwA4XA0GSIY/maxres.jpg","width":1280,"height":720},{"quality":"maxresdefault","url":"https://inv.nadeko.net/vi/mwA4XA0GSIY/maxresdefault.jpg","width":1280,"height":720},{"quality":"sddefault","url":"https://inv.nadeko.net/vi/mwA4XA0GSIY/sddefault.jpg","width":640,"height":480},{"quality":"high","url":"https://inv.nadeko.net/vi/mwA4XA0GSIY/hqdefault.jpg","width":480,"height":360},{"quality":"medium","url":"https://inv.nadeko.net/vi/mwA4XA0GSIY/mqdefault.jpg","width":320,"height":180},{"quality":"default","url":"https://inv.nadeko.net/vi/mwA4XA0GSIY/default.jpg","width":120,"height":90},{"quality":"start","url":"https://inv.nadeko.net/vi/mwA4XA0GSIY/1.jpg","width":120,"height":90},{"quality":"middle","url":"https://inv.nadeko.net/vi/mwA4XA0GSIY/2.jpg","width":120,"height":90},{"quality":"end","url":"https://inv.nadeko.net/vi/mwA4XA0GSIY/3.jpg","width":120,"height":90}],"author":"英検準1級×TOEIC820English×Village代表 タニヒト","authorUrl":"/channel/UCLmc9Bp4DV40Jve7hinIgoQ","authorId":"UCLmc9Bp4DV40Jve7hinIgoQ","authorVerified":false,"lengthSeconds":462,"viewCountText":"22K","viewCount":22682},{"videoId":"DQyH7jBD0hY","title":"Learn English quickly with Smart Podcast | Episode 15","videoThumbnails":[{"quality":"maxres","url":"https://inv.nadeko.net/vi/DQyH7jBD0hY/maxres.jpg","width":1280,"height":720},{"quality":"maxresdefault","url":"https://inv.nadeko.net/vi/DQyH7jBD0hY/maxresdefault.jpg","width":1280,"height":720},{"quality":"sddefault","url":"https://inv.nadeko.net/vi/DQyH7jBD0hY/sddefault.jpg","width":640,"height":480},{"quality":"high","url":"https://inv.nadeko.net/vi/DQyH7jBD0hY/hqdefault.jpg","width":480,"height":360},{"quality":"medium","url":"https://inv.nadeko.net/vi/DQyH7jBD0hY/mqdefault.jpg","width":320,"height":180},{"quality":"default","url":"https://inv.nadeko.net/vi/DQyH7jBD0hY/default.jpg","width":120,"height":90},{"quality":"start","url":"https://inv.nadeko.net/vi/DQyH7jBD0hY/1.jpg","width":120,"height":90},{"quality":"middle","url":"https://inv.nadeko.net/vi/DQyH7jBD0hY/2.jpg","width":120,"height":90},{"quality":"end","url":"https://inv.nadeko.net/vi/DQyH7jBD0hY/3.jpg","width":120,"height":90}],"author":"English Smart Podcast","authorUrl":"/channel/UCS5SY45nVDDAQTBmPCLGHbQ","authorId":"UCS5SY45nVDDAQTBmPCLGHbQ","authorVerified":false,"lengthSeconds":1013,"viewCountText":"94","viewCount":94},{"videoId":"SPQ5Vz4UaRA","title":"Simple Daily Use English Questions and Answers for Beginners - English Conversation Practice","videoThumbnails":[{"quality":"maxres","url":"https://inv.nadeko.net/vi/SPQ5Vz4UaRA/maxres.jpg","width":1280,"height":720},{"quality":"maxresdefault","url":"https://inv.nadeko.net/vi/SPQ5Vz4UaRA/maxresdefault.jpg","width":1280,"height":720},{"quality":"sddefault","url":"https://inv.nadeko.net/vi/SPQ5Vz4UaRA/sddefault.jpg","width":640,"height":480},{"quality":"high","url":"https://inv.nadeko.net/vi/SPQ5Vz4UaRA/hqdefault.jpg","width":480,"height":360},{"quality":"medium","url":"https://inv.nadeko.net/vi/SPQ5Vz4UaRA/mqdefault.jpg","width":320,"height":180},{"quality":"default","url":"https://inv.nadeko.net/vi/SPQ5Vz4UaRA/default.jpg","width":120,"height":90},{"quality":"start","url":"https://inv.nadeko.net/vi/SPQ5Vz4UaRA/1.jpg","width":120,"height":90},{"quality":"middle","url":"https://inv.nadeko.net/vi/SPQ5Vz4UaRA/2.jpg","width":120,"height":90},{"quality":"end","url":"https://inv.nadeko.net/vi/SPQ5Vz4UaRA/3.jpg","width":120,"height":90}],"author":"English Prince","authorUrl":"/channel/UCQHEXKJvHqO6ebIl4cMRJEg","authorId":"UCQHEXKJvHqO6ebIl4cMRJEg","authorVerified":false,"lengthSeconds":647,"viewCountText":"227","viewCount":227},{"videoId":"jTFxDrNel1E","title":"Practice for the interview test of Eiken 2nd grade & my horizontal bar skills! 英検２級面接試験の練習と鉄棒の技！","videoThumbnails":[{"quality":"maxres","url":"https://inv.nadeko.net/vi/jTFxDrNel1E/maxres.jpg","width":1280,"height":720},{"quality":"maxresdefault","url":"https://inv.nadeko.net/vi/jTFxDrNel1E/maxresdefault.jpg","width":1280,"height":720},{"quality":"sddefault","url":"https://inv.nadeko.net/vi/jTFxDrNel1E/sddefault.jpg","width":640,"height":480},{"quality":"high","url":"https://inv.nadeko.net/vi/jTFxDrNel1E/hqdefault.jpg","width":480,"height":360},{"quality":"medium","url":"https://inv.nadeko.net/vi/jTFxDrNel1E/mqdefault.jpg","width":320,"height":180},{"quality":"default","url":"https://inv.nadeko.net/vi/jTFxDrNel1E/default.jpg","width":120,"height":90},{"quality":"start","url":"https://inv.nadeko.net/vi/jTFxDrNel1E/1.jpg","width":120,"height":90},{"quality":"middle","url":"https://inv.nadeko.net/vi/jTFxDrNel1E/2.jpg","width":120,"height":90},{"quality":"end","url":"https://inv.nadeko.net/vi/jTFxDrNel1E/3.jpg","width":120,"height":90}],"author":"Marisa's English Adventure","authorUrl":"/channel/UCwbcobsHlcpXnCkhIEac6EQ","authorId":"UCwbcobsHlcpXnCkhIEac6EQ","authorVerified":false,"lengthSeconds":355,"viewCountText":"659","viewCount":659},{"videoId":"hvPQyeoSfFI","title":"英検2級 過去問 2024年第2回 (20) Coffee Culture","videoThumbnails":[{"quality":"maxres","url":"https://inv.nadeko.net/vi/hvPQyeoSfFI/maxres.jpg","width":1280,"height":720},{"quality":"maxresdefault","url":"https://inv.nadeko.net/vi/hvPQyeoSfFI/maxresdefault.jpg","width":1280,"height":720},{"quality":"sddefault","url":"https://inv.nadeko.net/vi/hvPQyeoSfFI/sddefault.jpg","width":640,"height":480},{"quality":"high","url":"https://inv.nadeko.net/vi/hvPQyeoSfFI/hqdefault.jpg","width":480,"height":360},{"quality":"medium","url":"https://inv.nadeko.net/vi/hvPQyeoSfFI/mqdefault.jpg","width":320,"height":180},{"quality":"default","url":"https://inv.nadeko.net/vi/hvPQyeoSfFI/default.jpg","width":120,"height":90},{"quality":"start","url":"https://inv.nadeko.net/vi/hvPQyeoSfFI/1.jpg","width":120,"height":90},{"quality":"middle","url":"https://inv.nadeko.net/vi/hvPQyeoSfFI/2.jpg","width":120,"height":90},{"quality":"end","url":"https://inv.nadeko.net/vi/hvPQyeoSfFI/3.jpg","width":120,"height":90}],"author":"元英語嫌い の英検チャンネル (Marshall Rising Sun English)","authorUrl":"/channel/UCUVexmgBC1CAetTAtUlDKKg","authorId":"UCUVexmgBC1CAetTAtUlDKKg","authorVerified":false,"lengthSeconds":820,"viewCountText":"79","viewCount":79},{"videoId":"uNNabiSB_DE","title":"Learn English With Podcast | Learn English fast | Episode 28","videoThumbnails":[{"quality":"maxres","url":"https://inv.nadeko.net/vi/uNNabiSB_DE/maxres.jpg","width":1280,"height":720},{"quality":"maxresdefault","url":"https://inv.nadeko.net/vi/uNNabiSB_DE/maxresdefault.jpg","width":1280,"height":720},{"quality":"sddefault","url":"https://inv.nadeko.net/vi/uNNabiSB_DE/sddefault.jpg","width":640,"height":480},{"quality":"high","url":"https://inv.nadeko.net/vi/uNNabiSB_DE/hqdefault.jpg","width":480,"height":360},{"quality":"medium","url":"https://inv.nadeko.net/vi/uNNabiSB_DE/mqdefault.jpg","width":320,"height":180},{"quality":"default","url":"https://inv.nadeko.net/vi/uNNabiSB_DE/default.jpg","width":120,"height":90},{"quality":"start","url":"https://inv.nadeko.net/vi/uNNabiSB_DE/1.jpg","width":120,"height":90},{"quality":"middle","url":"https://inv.nadeko.net/vi/uNNabiSB_DE/2.jpg","width":120,"height":90},{"quality":"end","url":"https://inv.nadeko.net/vi/uNNabiSB_DE/3.jpg","width":120,"height":90}],"author":"English learning wave","authorUrl":"/channel/UCudS5hLMpVj19PEa4JI8dGw","authorId":"UCudS5hLMpVj19PEa4JI8dGw","authorVerified":false,"lengthSeconds":919,"viewCountText":"436","viewCount":436}]}
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
