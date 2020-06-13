from flask import Flask, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import json
import geoip2.database
import os

from spiders.mysql_connection import activity_table, db_connection
#from server.fake_data import daily_recom, weekyly_new

print(os.getcwd())

app = Flask(__name__, static_url_path='/static', static_folder = "static")
app.config['SECRET_KEY'] = '20190515Q2AIKFC'

AUTH = 'Bearer 35ERHJUXK8CSL16OP40DWIZBQYGMFN96'
default_headers = {'authorization': AUTH}
keyword_list = ['大安區', '活動', '旅遊']

@app.route('/')
def hello():
    print(os.getcwd())
    post_url = 'http://localhost:5000/test_post'
    payload = "{'name': 'genius', 'age':'20'}"
    res = requests.post(post_url, data=payload)

    return 'Hello, world!'

@app.route('/home_info')
def home_info():
    res = {}

    sql_string = "SELECT title, DATE_FORMAT(date_time, '%Y/%m/%d') AS date_time, \
                price, location, address, description, category, image_url \
                FROM {db_table} WHERE address LIKE '%大安%' limit 10;" \
                .format(db_table=activity_table)
    activities = list(db_connection.execute_select(sql_string))
    res['daily_recom'] = activities
    print(activities)

    sql_string = "SELECT title, DATE_FORMAT(date_time, '%Y/%m/%d') AS date_time, \
                price, location, address, description, category, image_url \
                FROM {db_table} WHERE address LIKE '%信義%' AND \
                (address LIKE '%台北%' OR address LIKE '%臺北%') limit 10;" \
                .format(db_table=activity_table)
    activities = list(db_connection.execute_select(sql_string))
    res['weekyly_new'] = activities
    print(activities)

    print(res)
    # # 假資料 from fake_data.py
    # res['daily_recom'] = daily_recom
    # res['weekyly_new'] = weekyly_new
    return json.dumps(res)

@app.route('/<category>')
def return_category(category):
    res = {}

    # sql_string = "SELECT title, DATE_FORMAT(date_time, '%Y/%m/%d') AS date_time, \
    #             price, location, address, description, category, image_url \
    #             FROM {db_table} WHERE address LIKE '%大安%' AND category='{cat}' limit 10;" \
    #             .format(db_table=activity_table, cat=category)
    sql_string = "SELECT title, date_time, \
                price, location, address, description, category, image_url \
                FROM {db_table} WHERE category='{cat}' limit 10;" \
                .format(db_table=activity_table, cat=category)
    print(sql_string)
    activities = list(db_connection.execute_select(sql_string))
    res['daily_recom'] = activities
    print(activities)

    # sql_string = "SELECT title, DATE_FORMAT(date_time, '%Y/%m/%d') AS date_time, \
    #             price, location, address, description, category, image_url \
    #             FROM {db_table} WHERE address LIKE '%信義%' AND \
    #             (address LIKE '%台北%' OR address LIKE '%臺北%') AND \
    #             category='{cat}' limit 10;" \
    sql_string = "SELECT title, date_time, \
                price, location, address, description, category, image_url \
                FROM {db_table} WHERE category='{cat}' limit 10;" \
                .format(db_table=activity_table, cat=category)
    print(sql_string)
    activities = list(db_connection.execute_select(sql_string))
    res['weekyly_new'] = activities
    print(activities)

    print(res)
    # # 假資料 from fake_data.py
    # res['daily_recom'] = daily_recom
    # res['weekyly_new'] = weekyly_new
    return json.dumps(res)

@app.route('/login', methods=['GET', 'POST']) 
def login():
    if request.method == 'POST': 
        return 'Hello ' + request.values['username'] 

    return "<form method='post' action='/login'><input type='text' name='username' />" \
            "</br>" \
           "<button type='submit'>Submit</button></form>"

@app.route('/user_prefer', methods=['GET', 'POST'])
def user_prefer():
    """ get a prefer_list """
    print(request.values)
    if request.method == 'POST':
        prefer_list = request.values['prefer_list']
        prefer_list_join = '(' + ', '.join(prefer_list) + ')'
    else:
        prefer_list_join = "('健康')"

    sql_query = 'select * from `{}` where `category` in {} limit 5'\
        .format(activity_table, prefer_list_join)
    results = db_connection.execute_select(sql_query)

    return results

@app.route('/facebook/poi')
def facebook_poi():
    # 取得外部 IP
    ip = requests.get('https://api.ipify.org').text
    print('My public IP address is:', ip)

    # 由 IP 得知所在城市、經緯度等資訊
    reader = geoip2.database.Reader('geoip2/GeoLite2-City.mmdb')
    response = reader.city(ip)
    latitude = response.location.latitude
    longitude = response.location.longitude

    # target_url = 'https://workshop.ifeel.com.tw/facebook/poi/?latitude=24.15004&longitude=120.68451&name=活動'
    # 華南銀行國際會議廳，經緯度
    target_url = 'https://workshop.ifeel.com.tw/facebook/poi/?latitude={}&longitude={}'.format('25.0343863', '121.5689028')
    
    # # 代入該 user 所在的經緯度
    # target_url = 'https://workshop.ifeel.com.tw/facebook/poi/?latitude={}&longitude={}'.format(latitude, longitude)

    response = requests.get(target_url, headers=default_headers)
    
    hot_place = []
    for hot in response.json()['data']:
        if hot['event']['checkins'] > 1000:
            hot_place.append(hot['location']['name'])

    return_str = '您附近的熱門地點有 : <br/>' + '<br/>'.join(hot_place)
    return return_str
    # return json.dumps(response.json())

@app.route('/ptt')
def ptt():
    headers = default_headers.copy()
    headers['content-type'] = 'application/json'
    target_url = 'https://workshop.ifeel.com.tw/document/ptt/'

    data = {
        "date": '2018-01-02',
        "keyword": '活動'
    }

    response = requests.post(target_url, headers=headers, data=json.dumps(data))
    return json.dumps(response.json())