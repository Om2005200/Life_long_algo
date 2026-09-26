import pandas as pd
import csv
import json 

from datetime import datetime 
import time 



class ORB_CODE:
    def __init__(self):
        pass


    def opening_the_raw_file(self):
        with open(r"C:\Users\dasho\divergence_test.json",'r') as cv:
            data=json.load(cv)
            return data



    def analyzing_the_data(self):
        main_data=self.opening_the_raw_file()
        master_closed_data=[]
        orb_candle=[]

        latest_date="2026-09-17"
        for datas in main_data:
            current_close=datas['CLOSE']
            current_open=datas['OPEN']
            current_time=datas['TIME']
            current_date=datas['DATE']
            current_low=datas['LOW']
            current_high=datas['HIGH']
            master_closed_data.append(current_close)
            if current_date==latest_date:


                if current_time=='09:15':
                    orb_candle.append(datas)
        print(orb_candle)
                    

            
o=ORB_CODE()
o.opening_the_raw_file()
o.analyzing_the_data()
