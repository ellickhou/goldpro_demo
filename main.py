# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 15:39:37 2019

@author: dear983604
"""

from pygame import mixer
import time
import Gold_pro_class as Gpc

mixer.init()

check_out = False

#導入Gold_pro裡的class
GP = Gpc.Gold_pro()

    
time.sleep(2)

while not GP.check_out:    
    GP.listen()
    GP.analysis()

GP.checkOut()    
    


