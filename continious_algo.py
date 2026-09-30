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

        latest_date="2026-09-30"
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
        for orb in orb_candle:
            orb_high=orb['HIGH']
            orb_low=orb['LOW']



        original_closing_prices=master_closed_data[-1]
        for data in main_data:
            data_close=data['CLOSE']
            data_open=data['OPEN']
            data_date=data['DATE']
            data_time=data['TIME']
            if current_date==data_date:
                if data_close==original_closing_prices:

                    if data_close<data_open:
                        first_red_candle=[]
                        for candles in main_data:
                            candle_close=candles['CLOSE']
                            candle_open=candles['OPEN']
                            candle_date=candles['DATE']
                            candle_time=candles['TIME']
                            if candle_date==current_date:
                                if original_closing_prices==candle_close:

                                    if candle_close<candle_open:
                                        first_red_candle.append(candles)
                                        first_value_red_candle=first_red_candle[-1]


                        if first_value_red_candle is not None:
                            first_value_red_candle_close=first_value_red_candle['CLOSE']
                            first_value_red_candle_time=first_value_red_candle['TIME']
                            first_value_red_candle_low=first_value_red_candle['LOW']
                            first_value_red_candle_open=first_value_red_candle['OPEN']




                        ###################  TO FIND THE CONSOLIDATION LEVELS ########################
                        consolidation_candle=[]
                        for new_candles in main_data:
                            new_close=new_candles['CLOSE']
                            new_open=new_candles['OPEN']
                            new_date=new_candles['DATE']
                            new_low=new_candles['LOW']
                            if new_date==latest_date:
                                if new_close==first_value_red_candle_close or first_value_red_candle_low==new_low or first_value_red_candle_low==new_close or new_open<=first_value_red_candle_open and new_close<=first_value_red_candle_open and new_open>first_value_red_candle_close or new_open<=first_value_red_candle_close and new_close<=first_value_red_candle_open:



                                    consolidation_candle.append(new_candles)
                   


   ############ GREEN_CANDLES #########
                        ######################################## RETEST CANDLE ##########################

                    elif data_close>data_open:
                        retest_candle=[]
                        for second_level in main_data:
                            second_date=second_level['DATE']
                            second_open=second_level['OPEN']
                            second_close=second_level['CLOSE']
                            second_time=second_level['TIME']
                            second_low=second_level['LOW']
                            second_high=second_level['HIGH']



                            if second_date==current_date:
                                if original_closing_prices==second_close:
                                    if second_close>second_open:
                                        if second_low<=orb_low and second_close>orb_low    or second_low<=orb_high and second_close>orb_high and second_open>orb_high:
                                            #print(second_level)
                                            retest_candle.append(second_level)


                        ###########################################  LIQUIDITY SWEEP CANDLES ##############


                        third_level_green_candle=[]
                        for third_level_candle in main_data:
                            third_level_close=third_level_candle['CLOSE']
                            third_level_open=third_level_candle['OPEN']
                            third_level_date=third_level_candle['DATE']
                            third_level_time=third_level_candle['TIME']
                            third_level_low=third_level_candle['LOW']
                            third_level_high=third_level_candle['HIGH']

                            if current_date==third_level_date:
                                if third_level_close==original_closing_prices:

                                    if third_level_close>third_level_open:
                                        open_low=third_level_open-third_level_low
                                        open_close=third_level_close-third_level_open
                                        high_close=third_level_high-third_level_close


                                        
                                        if open_low>open_close and open_close>high_close:
                                            third_level_green_candle.append(third_level_candle)
                                            #print(third_level_candle)


                        fourth_level_candle_breakout=[]
                        fourth_level_candle_retest=[]


                        for retest_candle_ in main_data:
                            retest_candle_close=retest_candle_['CLOSE']
                            retest_candle_open=retest_candle_['OPEN']
                            retest_candle_date=retest_candle_['DATE']
                            retest_candle_high=retest_candle_['HIGH']
                            retest_candle_low=retest_candle_['LOW']
                            if current_date==retest_candle_date:
                                if retest_candle_close==original_closing_prices:

                                    if retest_candle_close>retest_candle_open:
                                        if retest_candle_open==orb_high and retest_candle_close>orb_high or retest_candle_close>orb_high and retest_candle_open>orb_high and retest_candle_low<orb_high:
                                            fourth_level_candle_retest.append(retest_candle_)
                        if fourth_level_candle_retest:
                            for levels in fourth_level_candle_retest:

                                fourth_time=levels['TIME']
                        else:
                            print('NOT A VALID SETUP')
                            return

                        
                        for fourth_level_candle in main_data:
                            fourth_level_candle_close=fourth_level_candle['CLOSE']
                            fourth_level_candle_open=fourth_level_candle['OPEN']
                            fourth_level_candle_date=fourth_level_candle['DATE']
                            fourth_level_candle_time=fourth_level_candle['TIME']
                            fourth_level_candle_low=fourth_level_candle['LOW']
                            fourth_level_candle_high=fourth_level_candle['HIGH']
                            if current_date==fourth_level_candle_date:
                                    if fourth_level_candle_time<fourth_time:
                                        

                                
                                        if fourth_level_candle_close>fourth_level_candle_open:
                                            if fourth_level_candle_close>orb_high and fourth_level_candle_open<orb_high:
                                                fourth_level_candle_breakout.append(fourth_level_candle)

                                                only_candle=fourth_level_candle_breakout[-1]


                        if only_candle is not None:
                            print(only_candle)
                            


                        
                                            
                                    

                            





                

                            

                                

                    

            
o=ORB_CODE()
o.opening_the_raw_file()
o.analyzing_the_data()
