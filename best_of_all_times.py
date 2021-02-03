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
new_sheet = gss_client.open_by_key(spreadsheet_key).add_worksheet(title="best_of_all_times", rows="2500", cols="20")

# 搜尋 URL
steam_url = 'https://steam250.com/old'

main_array = [['' for x in range(20)] for x in range(2500)]

# 下載結果
r = requests.get(steam_url)

# 確認是否下載成功
if r.status_code == requests.codes.ok:
  # 以 BeautifulSoup 解析 HTML 原始碼
  soup = BeautifulSoup(r.text, 'html.parser')

  # 查詢歷年資料 URL
  year_div = soup.find("div", class_="timeline")
  href_tag = year_div.find_all("a")
  print(len(href_tag))
  year_idx = 0
  now_url_year = href_tag[year_idx]['href']
  rows = 1

  main_array[0][0] = "Game Name"
  main_array[0][1] = "Image URL"
  main_array[0][19] = "Total"

  while(year_idx < len(href_tag)):
    main_array[0][2+year_idx] = href_tag[year_idx].text
    year_request = requests.get(steam_url.replace(now_url_year, href_tag[year_idx]['href']))
    print(steam_url.replace(now_url_year, href_tag[year_idx]['href']))
    year_soup = BeautifulSoup(year_request.text, 'html.parser')

    # 觀察 HTML 原始碼
    rank_div = year_soup.find("div", class_="main ranking")
    title_tag = rank_div.find_all("span", class_="title")
    img_tag = rank_div.find_all("img")
    votes_tag = rank_div.find_all("span", class_="votes")
    
    i = 0
    while(i < len(title_tag)):
      print(rows + i)
      main_array[rows + i][0] = title_tag[i].a.text
      i += 1
    k = 0
    while(k < len(img_tag)):
      main_array[rows + k][1] = "https:" + img_tag[k]['src']
      main_array[rows + k][2+year_idx] = 0
      k += 1
    r = 0
    while(r < len(votes_tag)):
      main_array[rows + r][19] = int(votes_tag[r].text.replace(" votes", "").replace(",", ""))
      r += 1
    rows += len(title_tag)
    year_idx += 1

  print(main_array)
  new_sheet.update('A1:T2500', main_array)