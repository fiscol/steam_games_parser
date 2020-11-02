# -*- coding: UTF-8 -*-

# 引入 Beautiful Soup 模組
from bs4 import BeautifulSoup
import re
import requests
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials

auth_json_path = 'auth_token.json'
gss_scopes = ['https://spreadsheets.google.com/feeds']
#連線
credentials = ServiceAccountCredentials.from_json_keyfile_name(auth_json_path,gss_scopes)
gss_client = gspread.authorize(credentials)
#開啟 Google Sheet 資料表
spreadsheet_key = '1jVAgY8bbEuw3c7ySSh6-Y_Ux7OzlXict8PPPZ_9iPE8'
#取得目前工作分頁的長度
new_sheet_id = str(len(gss_client.open_by_key(spreadsheet_key).worksheets()) + 1)
#建立新工作分頁
new_sheet = gss_client.open_by_key(spreadsheet_key).add_worksheet(title="工作表" + new_sheet_id, rows="250", cols="5")

# 搜尋 URL
steam_url = 'https://steam250.com/most_played'

# 下載結果
r = requests.get(steam_url)

# 確認是否下載成功
if r.status_code == requests.codes.ok:
  # 以 BeautifulSoup 解析 HTML 原始碼
  soup = BeautifulSoup(r.text, 'html.parser')

  # 觀察 HTML 原始碼
  rank_div = soup.find("div", class_="main ranking")
  title_tag = rank_div.find_all("span", class_="title")
  release_tag = rank_div.find_all("span", class_="date")
  img_tag = rank_div.find_all("img")
  players_tag = rank_div.find_all("span", class_="players")
  movement_tag = rank_div.find_all("span", class_="movement")
  main_array = [[0 for x in range(5)] for x in range(250)]

  print(len(title_tag))
  print(len(release_tag))
  
  i = 0
  while(i < len(title_tag)):
    main_array[i][0] = title_tag[i].a.text
    i += 1
  j = 0
  while(j < len(release_tag)):
    main_array[j][1] = release_tag[j].text[1:].rstrip()
    j += 1
  k = 0
  while(k < len(img_tag)):
    main_array[k][2] = "https:" + img_tag[k]['src']
    k += 1
  r = 0
  while(r < len(players_tag)):
    main_array[r][3] = int(players_tag[r].text.replace(",", ""))
    r += 1
  s = 0
  m = 1
  while(s < len(movement_tag)):
    if movement_tag[s]['title'] == 'Moved down':
      main_array[s][4] = s + 1 - int(movement_tag[s].text)
    elif movement_tag[s]['title'] == 'Moved up':
      main_array[s][4] = s + 1 + int(movement_tag[s].text)
    elif movement_tag[s]['title'] == 'New entry':
      main_array[s][4] = "New"
      m += 1
    else:
      main_array[s][4] = s + 1
    s += 1
  print(main_array)
  new_sheet.update('A1:E250', main_array)