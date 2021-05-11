# -*- coding: UTF-8 -*-

# 引入 Beautiful Soup 模組
from bs4 import BeautifulSoup
import re
import requests
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials

auth_json_path = 'datakid_auth_token.json'
gss_scopes = ['https://spreadsheets.google.com/feeds']
#連線
credentials = ServiceAccountCredentials.from_json_keyfile_name(auth_json_path,gss_scopes)
gss_client = gspread.authorize(credentials)
#開啟 Google Sheet 資料表
spreadsheet_key = '1JaDidRTxi0s6UHWNSLiPL4QaCmYn-_ysMdlhU85YrFs'
#建立新工作分頁
new_sheet = gss_client.open_by_key(spreadsheet_key).add_worksheet(title="best_of_2020", rows="150", cols="15")

# 搜尋 URL
steam_url = 'https://steam250.com/2020'

main_array = [['' for x in range(15)] for x in range(151)]

# 下載結果
r = requests.get(steam_url)

# 確認是否下載成功
if r.status_code == requests.codes.ok:
  # 以 BeautifulSoup 解析 HTML 原始碼
  soup = BeautifulSoup(r.text, 'html.parser')

  main_array[0][0] = "Game Name"
  main_array[0][1] = "Image URL"
  main_array[0][14] = "Total"

  month_arr = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

  for i in range(0, len(month_arr)):
    main_array[0][i+2] = month_arr[i]

  # 觀察 HTML 原始碼
  rank_div = soup.find("div", class_="main ranking")
  title_tag = rank_div.find_all("span", class_="title")
  release_tag = rank_div.find_all("span", class_="date")
  img_tag = rank_div.find_all("img")
  votes_tag = rank_div.find_all("span", class_="votes")
    
  i = 0
  while(i < len(title_tag)):
    main_array[i+1][0] = title_tag[i].a.text
    i += 1
  j = 0
  while(j < len(release_tag)):
    month_idx = 0
    if(release_tag[j].text[1:].rstrip().split()[1] == "2020"):
      month_idx = month_arr.index(release_tag[j].text[1:].rstrip().split()[0])
    else:
      month_idx = month_arr.index("Dec")
    main_array[j+1][2+month_idx] = 0
    j += 1
    k = 0
    while(k < len(img_tag)):
      main_array[k+1][1] = "https:" + img_tag[k]['src']
      k += 1
    r = 0
    while(r < len(votes_tag)):
      main_array[r+1][14] = int(votes_tag[r].text.replace(" votes", "").replace(",", ""))
      r += 1
  
  print(main_array)
  new_sheet.update('A1:O151', main_array)