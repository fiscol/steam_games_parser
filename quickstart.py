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
#建立工作表1
# sheet = gss_client.open_by_key(spreadsheet_key).sheet1
#主工作表名稱
main_sheet = gss_client.open_by_key(spreadsheet_key).worksheet('工作表1')
#取得目前工作分頁的長度
new_sheet_id = "工作表" + str(len(gss_client.open_by_key(spreadsheet_key).worksheets()))
#讀取當日最新工作表資料
latest_sheet = gss_client.open_by_key(spreadsheet_key).worksheet(new_sheet_id)
# Google Sheet 資料表操作(舊版)
# sheet.clear() # 清除 Google Sheet 資料表內容
# listtitle=["姓名","電話"]
# sheet.append_row(listtitle)  # 標題
# listdata=["Liu","0912-345678"]
# sheet.append_row(listdata)  # 資料內容
# #Google Sheet 資料表操作(20191224新版)
# sheet.update_acell('D2', 'ABC')  #D2加入ABC
# sheet.update_cell(2, 4, 'ABC')   #D2加入ABC(第2列第4行即D2)
# #寫入一整列(list型態的資料)
# values = ['A','B','C','D']
# sheet.insert_row(values, 1) #插入values到第1列
#讀取儲存格
# sheet.acell('B1').value
# sheet.cell(1, 2).value
#讀取整欄或整列
# print(main_sheet.row_values(1)) #讀取第1列的一整列
today_column = len(main_sheet.row_values(2)) + 1
# today_column = len(main_sheet.row_values(2))
total_saved_rows = len(main_sheet.col_values(1))
# print(total_saved_rows)
# saved_game_names = main_sheet.col_values(1) #讀取第1欄的一整欄
#讀取整個表
second = latest_sheet.get_all_values()

# print(len(second))
# print(second[0][0])
for i in range(0, 250):
  while True:
    try:
      cell = main_sheet.find(second[i][0])
      print('#' + str(cell.row - 1) + " -> #" + str(i + 1))
      if (main_sheet.cell(cell.row, 2).value != second[i][1]):
        main_sheet.update_cell(cell.row, 2, second[i][1])
      if (main_sheet.cell(cell.row, 3).value != second[i][2]):
        main_sheet.update_cell(cell.row, 3, second[i][2])
      main_sheet.update_cell(cell.row, today_column, second[i][3])
    except gspread.exceptions.CellNotFound:
      print("New Data")
      total_saved_rows+=1
      new_data=[second[i][0],second[i][1],second[i][2]]
      main_sheet.append_row(new_data)
      main_sheet.update_cell(total_saved_rows, today_column, second[i][3])
    except gspread.exceptions.APIError:
      print("#" + str(i + 1) + " Sleep until sheet quota is being reset.")
      continue
    break