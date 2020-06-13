# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 23:32:20 2019

@author: dear9
"""
#參考來源 https://github.com/maotingyang/Coffee-Bot

import speech_recognition as sr
from gtts import gTTS    
from pygame import mixer
import tempfile
import jieba
import time
import requests
mixer.init()

server_url = 'http://localhost:5000/'

#活動分類
activity_list = [
    '旅遊','藝文','講座','親子','健康',
    '手作麵包','跑步小聚','達文西'
]

response = ['收藏','提醒']
s = requests.session()
s.keep_alive = False

item_list = []


class Gold_pro():
    def __init__(self):
        self.check_out = False
        
    def speak(self, sentence):
        with tempfile.NamedTemporaryFile(delete=True) as fp:
            tts = gTTS(text=sentence, lang='zh-tw')
            tts.save("{}.mp3".format(fp.name))
            mixer.music.load('{}.mp3'.format(fp.name))
            mixer.music.play()
            while mixer.music.get_busy():
                pass
            
    def listen(self):
        global item_list
        r = sr.Recognizer()
        with sr.Microphone(device_index=0) as source:
            print('bot listening...')
            audio = r.listen(source)
            print('bot processing...')
            # time.sleep(2)
        try:
            self.customer_schedule = r.recognize_google(audio, language='zh-TW')
            print("Google Speech Recognition thinks you said " + self.customer_schedule)
        
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            self.listen()
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    def analysis(self):
        customer_schedule = self.customer_schedule
        if '返回' in customer_schedule : 
            print('結束')
            global check_out
            self.check_out = True
            
        elif '活動' in customer_schedule:
            Gold_pro_str='好的，馬上為您呈現。已為您挑選了今日及本週精彩內容，請問您對哪個有興趣呢'
            print('Gold Pro: '+Gold_pro_str)
            self.speak(Gold_pro_str)
        
        elif '清單' in customer_schedule:
            print('好的主人，這些是您收藏的活動。您可以大聲告訴我活動名稱，了解活動內容並設定提醒')
            self.speak('好的主人，這些是您收藏的活動。您可以大聲告訴我活動名稱，了解活動內容並設定提醒')
            
            #time.sleep(2)
        elif '開啟' in customer_schedule:
            print('已為您開啟Good idea好主意 Kevin老師 早午餐系列課程，請問要加入收藏嗎')
            self.speak('已為您開啟Good idea好主意 Kevin老師 早午餐系列課程，請問要加入收藏嗎')

        else:
            seg_list = jieba.cut(customer_schedule, cut_all=False)
            print(','.join(seg_list))
            info = {}
            for word in seg_list:
                print(word)
                # 找出數量詞
            print(customer_schedule)
            if '不用' in customer_schedule:
                print("您可繼續看看最近還有哪些活動")
                self.speak("您可繼續看看最近還有哪些活動")

            name_counts = len(activity_list)  # 活動種類
            for name in activity_list:
                if name_counts == 0:
                    self.speak('目前尚無提供該項活動')
                elif name in customer_schedule:
                    info['行程'] = name 
                    # info['地點'] = location
                    print(info)
                    item_list.append(info)
                    print(item_list)
                    if '手作麵包' in customer_schedule:
                        print("Gold Pro: 主人真會選，這個行程很熱門，為您提供",name,"的訊息，今天下午2點在非凡早餐店，請問要加入收藏嗎")
                        self.speak("主人真會選，這個行程很熱門，為您提供{}的訊息，今天下午2點在非凡早餐店，請問要加入收藏嗎"
                                .format(info.get('行程'), info.get('地點')))

                    else:

                        target_url = server_url + name
                        s.keep_alive = False
                        result = s.get(target_url)
                        # print(result.json())
                        result = result.json()['daily_recom'][0]
                        # print(result)
                        result_text = 'Gold Pro: 為您提供"{}"的訊息，活動 : {}；時間 : {}；地點 : {}，是否要加入提醒' \
                            .format(name, result['title'], result['date_time'], result['location'])
                        print(result_text)
                        self.speak(result_text)
                        # print(result['daily_recom'])
                        
                    # else:
                    #     print("Gold Pro:",name,"展覽，5月10日到31日在圓山文化基金會舉辦，請問要加入提醒嗎")
                    #     self.speak("{}展覽，5月10日到31日在圓山文化基金會舉辦，是否要加入提醒"
                    #         .format(info.get('行程')))
                        
                
                name_counts -= 1
                
            response_counts = len(response)  # 活動種類
            for answer in response:
                if response_counts == 0:
                    self.speak('目前尚無提供該項活動')
                elif answer in customer_schedule:
                    info['回答'] = answer 
#                    info['地點'] = location
                    print(info)
                    item_list.append(info)
                    print(item_list)
                    if '收藏' in customer_schedule:
                        print("已加入收藏清單")
                        self.speak("已加入收藏清單")
                    elif '提醒' in customer_schedule:
                        print("已將活動訊息寄簡訊給您")
                        self.speak('已將活動訊息寄簡訊給您')
                    else:
                        print("您可繼續看看最近還有哪些活動")
                        self.speak("您可繼續看看最近還有哪些活動")
                        
                
                response_counts -= 1

    def checkOut(self):
        if self.check_out == True:
            self.speak('沒問題')
            time.sleep(5)
    
