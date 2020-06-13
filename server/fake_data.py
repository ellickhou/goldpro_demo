from flask import Flask,jsonify
import requests
import json
import geoip2.database

app = Flask(__name__)


def return_img_stream(img_local_path):
    """
        工具函数:
        获取本地图片流
        :param img_local_path:文件单张图片的本地绝对路径
        :return: 图片流
        """
    import base64
    img_stream = ''
    with open(img_local_path, 'r') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream)



AUTH = 'Bearer 35ERHJUXK8CSL16OP40DWIZBQYGMFN96'
default_headers = {'authorization': AUTH}
keyword_list = ['大安區', '活動', '旅遊']
daily_recom = [
         {
         'title': u'手作麵包1',
         'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
         'date':'2019-04-01',
         'contact_info':'000000000',
         'location':'taipei',
         'image':u'http://localhost:5000/images/test.jpg'
         },
         {
         'title': u'手作麵包2',
         'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
         'date':'2019-04-02',
         'contact_info':'000000000',
         'location':'taipei',
         'image':u'http://localhost:5000/images/test.jpg'
         },
         {
         'title': u'手作麵包3',
         'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
         'date':'2019-04-03',
         'contact_info':'000000000',
         'location':'taipei',
         'image':u'None'
         },
         {
         'title': u'手作麵包4',
         'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
         'date':'2019-04-04',
         'contact_info':'000000000',
         'location':'taipei',
         'image':u'None'
         },
         {
         'title': u'手作麵包5',
         'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
         'date':'2019-04-05',
         'contact_info':'000000000',
         'location':'taipei',
         'image':u'None'
         },
         {
         'title': u'手作麵包6',
         'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
         'date':'2019-04-06',
         'contact_info':'000000000',
         'location':'taipei',
         'image':u'None'
         },
         {
         'title': u'手作麵包7',
         'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
         'date':'2019-04-07',
         'contact_info':'000000000',
         'location':'taipei',
         'image':u'None'
         },
         {
         'title': u'手作麵包8',
         'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
         'date':'2019-04-08',
         'contact_info':'000000000',
         'location':'taipei',
         'image':u'None'
         },
         {
         'title': u'手作麵包9',
         'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
         'date':'2019-04-09',
         'contact_info':'000000000',
         'location':'taipei',
         'image':u'None'
         },
         ]
weekyly_new = [
               {
               'title': u'音樂會1',
               'description': u'周杰倫',
               'date':'2019-05-01',
               'contact_info':'000000000',
               'location':'taipei',
               'image':u'None'
               },
               {
               'title': u'音樂會2',
               'description': u'A_lin',
               'date':'2019-05-02',
               'contact_info':'000000000',
               'location':'taipei',
               'image':u'None'
               },
               {
               'title': u'音樂會3',
               'description': u'紅髮ed',
               'date':'2019-05-03',
               'contact_info':'000000000',
               'location':'taipei',
               'image':u'None'
               },
               {
               'title': u'音樂會4',
               'description': u'陶喆',
               'date':'2019-05-04',
               'contact_info':'000000000',
               'location':'taipei',
               'image':u'None'
               },
               {
               'title': u'音樂會5',
               'description': u'bigbang',
               'date':'2019-05-05',
               'contact_info':'000000000',
               'location':'taipei',
               'image':u'None'
               },
               {
               'title': u'音樂會6',
               'description': u'twice',
               'date':'2019-05-06',
               'contact_info':'000000000',
               'location':'taipei',
               'image':u'None'
               },
               {
               'title': u'音樂會7',
               'description': u'五月天',
               'date':'2019-05-07',
               'contact_info':'000000000',
               'location':'taipei',
               'image':u'None'
               },
               {
               'title': u'音樂會8',
               'description': u'BTS',
               'date':'2019-05-08',
               'contact_info':'000000000',
               'location':'taipei',
               'image':u'None'
               },
              ]
@app.route('/home_info')
def home_info():
    return jsonify({'daily_recom': daily_recom,'weekyly_new':weekyly_new})

@app.route('/')
def hello():
    '''
    img_path = 'https://applealmond.com/wp-content/uploads/2017/06/1538237709-1cfcda1388073143c3e8615953bd7768.png'
    img_stream = return_img_stream(img_path)
    return render_template('index.html',img_stream=img_stream)
    '''
    return 'Hello, world!'

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
