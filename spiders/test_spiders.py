import requests
import json
from mysql_connection import db_connection, activity_table

headers = {'authorization': 'Bearer 35ERHJUXK8CSL16OP40DWIZBQYGMFN96'}

# # ~~~~~~~~~~~~~~~ accupass
# target_url = 'https://old.accupass.com/search/r/1/4/0/0/4/0/00010101/99991231'
# response = requests.get(target_url)
# print(response.content)


# # ~~~~~~~~~~~~~~~ FB poi (打卡資訊)
# # target_url = 'https://workshop.ifeel.com.tw/facebook/poi/?latitude=24.15004&longitude=120.68451&name=%E6%8B%89%E9%BA%B5&='
# target_url = 'https://workshop.ifeel.com.tw/facebook/poi/?latitude=24.15004&longitude=120.68451&name=活動'

# response = requests.get(target_url, headers=headers)
# print(response.json())

# # ~~~~~~~~~~~~~~~~ PTT
# headers['content-type'] = 'application/json'
# target_url = 'https://workshop.ifeel.com.tw/document/ptt/'

# data = {
#     "date": '2019-01-02',
#     "keyword": '講座'
# }

# response = requests.post(target_url, headers=headers, data=json.dumps(data))
# print(response.json())

# # ~~~~~~~~~~~~~~~~~ FB group
# headers['content-type'] = 'application/json'
# target_url = 'https://workshop.ifeel.com.tw/document/facebook/'

# data = {
#     "date": '2019-01-02',
#     "keyword": '悟覺妙天：宇宙の超生命'
# }

# response = requests.post(target_url, headers=headers, data=json.dumps(data))
# print(response.json())


sql_query = 'select * from `{}` where `category` in ("健康") limit 5'\
    .format(activity_table)
results = db_connection.execute_select(sql_query)

print(type(results)) # tuple
for row in results:
    print(row) # tuple
    print(row[1])