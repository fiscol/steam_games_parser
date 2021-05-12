Steam x YouTube parser 程式
  
# Install:  

```
需要先確認已安裝python3

安裝pip
>> curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
>> python3 get-pip.py --force-reinstall

確認pip3版本
>> pip3 -V

安裝相關套件
>> pip3 install -r requirements.txt 

跑YouTube爬蟲前需要安裝套件的指令
>> sudo pip install --upgrade google-api-python-client

```

# Run:

```
1. 執行Steam爬蟲程式
（基本上現在都是每天下班後，手動執行這個指令抓資料）
>> python3 daily_most_played_games.py && python3 daily_trending_games.py


2. 執行YouTube爬蟲程式
（目前不是全自動化的，所以需要執行下列的一些oauth權限同意授權操作）
>> python3 weekly_youtube_music_charts.py

後續會跳出一段類似下列範例，關於Oauth認證的網址，複製『網址段落』至瀏覽器打開：
Please visit this URL to authorize this application: https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=1093048110419-rq4crmpov8b26jr9lqu6rgnbef6haa2p.apps.googleusercontent.com&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.readonly&state=glq7qFiVG1I96OTqc50eWPj6yYreEY&prompt=consent&access_type=offline

然後同意相關權限，其中有一個頁面『這個應用程式未經 Google 驗證』，需要按下『進階』，點選『前往「Quickstart」(不安全)』，然後同意相關授權，最後會出現一段認證碼，複製至Terminal後面貼上：
>> Enter the authorization code: 

完成後爬到的JSON資料會寫至
youtube_music_data.json

可以將這個檔案複製至JSON Editor網站確認資料結構
https://jsoneditoronline.org/

```

# 相關檔案附註:

```
Steam相關的檔案：
daily_most_played_games.py
daily_trending_games.py

目前這兩個檔案讀寫的GCP權證檔案都是
datakid_auth_token.py

有一隻是lambda之前嘗試串接用的檔案，但後來還沒有空佈建上去
lambda_daily_most_played_games.py

相關套件：
requirements.txt

測試YouTube API的爬蟲程式檔案：
weekly_youtube_music_charts.py

上面這隻讀寫的GCP憑證檔案是
youtube-data.json

目前程式抓到的範例檔案是
youtube_music_data.json

至於bk_old資料夾裡面的是之前測試用的檔案，
可以暫時不看沒關係。

```