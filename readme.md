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

```

# Run:

```
執行Steam爬蟲程式
（基本上現在都是每天下班後，手動執行這個指令抓資料）
>> python3 daily_most_played_games.py && python3 daily_trending_games.py

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

至於bk_old資料夾裡面的是之前測試用的檔案，
可以暫時不看沒關係。

```