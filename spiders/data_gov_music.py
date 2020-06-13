import requests
from mysql_connection import db_connection, activity_table

target_url = 'https://cloud.culture.tw/frontsite/trans/SearchShowAction.do?method=doFindTypeJ&category=1'
res = requests.get(target_url)
# print(res.json())

for act in res.json():
    info = {}
    info['title'] = act['title']
    info['description'] = act['discountInfo']
    info['category'] = '藝文'
    info['image_url'] = info.get('imageUrl')

    for show in act['showInfo']:
        info['date_time'] = show['time']
        info['price'] = show['price']
        info['location'] = show['locationName']
        info['address'] = show['location']
        info['latitude'] = show['latitude']
        info['longitude'] = show['longitude']

        db_connection.update_or_insert(info, activity_table)
