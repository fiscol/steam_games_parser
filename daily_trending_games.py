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
#取得目前工作分頁的長度
new_sheet_id = str(len(gss_client.open_by_key(spreadsheet_key).worksheets()) + 1)
#建立新工作分頁
new_sheet = gss_client.open_by_key(spreadsheet_key).add_worksheet(title="工作表" + new_sheet_id, rows="50", cols="3")

# 搜尋 URL
steam_url = 'https://steam250.com/trending'

# 下載結果
r = requests.get(steam_url)

# 確認是否下載成功
if r.status_code == requests.codes.ok:
  # 以 BeautifulSoup 解析 HTML 原始碼
  soup = BeautifulSoup(r.text, 'html.parser')

  # 觀察 HTML 原始碼
  rank_div = soup.find("div", class_="main ranking")
  title_tag = rank_div.find_all("span", class_="title")
  img_tag = rank_div.find_all("img")
  velocity_tag = rank_div.find_all("span", class_="velocity")
  main_array = [[0 for x in range(3)] for x in range(50)]

  print(len(velocity_tag))
  
  i = 0
  while(i < len(title_tag)):
    main_array[i][0] = title_tag[i].a.text
    i += 1
  k = 0
  while(k < len(img_tag)):
    main_array[k][1] = "https:" + img_tag[k]['data-src']
    k += 1
  r = 0
  while(r < len(velocity_tag)):
    main_array[r][2] = int(velocity_tag[r].text.replace("velocity", "").replace(",", ""))
    r += 1
  print(main_array)
  new_sheet.update('A1:E50', main_array)

  #寫入總表

  #主工作表名稱
  main_sheet = gss_client.open_by_key(spreadsheet_key).worksheet('STEAM Trending Games 2021 May')
  #取得目前工作分頁的長度
  new_sheet_id = "工作表" + str(len(gss_client.open_by_key(spreadsheet_key).worksheets()))
  #讀取當日最新工作表資料
  latest_sheet = gss_client.open_by_key(spreadsheet_key).worksheet(new_sheet_id)
  #讀取整欄或整列
  if len(main_sheet.row_values(2)) != 0:
    today_column = len(main_sheet.row_values(2)) + 1
  else:
    today_column = 2 + 1
  total_saved_rows = len(main_sheet.col_values(1))
  #讀取整個表
  second = latest_sheet.get_all_values()
  #移除新工作表
  gss_client.open_by_key(spreadsheet_key).del_worksheet(latest_sheet)

  for i in range(0, 50):
    while True:
      try:
        cell = main_sheet.find(second[i][0])
        print('#' + str(cell.row - 1) + " -> #" + str(i + 1))
        if (main_sheet.cell(cell.row, 2).value != second[i][1]):
          main_sheet.update_cell(cell.row, 2, second[i][1])
        main_sheet.update_cell(cell.row, today_column, second[i][2])
      except gspread.exceptions.CellNotFound:
        print("New Data")
        total_saved_rows+=1
        new_data=[second[i][0],second[i][1]]
        main_sheet.append_row(new_data)
        main_sheet.update_cell(total_saved_rows, today_column, second[i][2])
        for m in range(3, today_column):
          main_sheet.update_cell(total_saved_rows, m, 0)
      except gspread.exceptions.APIError:
        print("#" + str(i + 1) + " Sleep until sheet quota is being reset.")
        continue
      break
  for n in range(2, total_saved_rows):
    while True:
      try:
        if (main_sheet.cell(n, today_column).value == ""):
          print('#' + str(n - 1) + " -> out of rankings")
          main_sheet.update_cell(n, today_column, 0)
      except gspread.exceptions.APIError:
        print("#" + str(n - 1) + " Sleep until sheet quota is being reset.")
        continue
      break
        