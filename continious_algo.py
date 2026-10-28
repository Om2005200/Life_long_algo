import pandas as pd
import csv
import json 

from datetime import datetime 
import time 



class ORB_CODE:
    def __init__(self):
        self.latest_date="2026-10-28"


    def opening_the_raw_file(self):
        with open(r"C:\Users\dasho\divergence_test.json",'r') as cv:
            data=json.load(cv)
            return data


     
    def opening_the_order_log(self):

        file_path = r'C:\Users\dasho\fvg_orderbook'


        try:
            with open(file_path, 'r') as x:
                data = json.load(x)

                # if file somehow contains null
                if data is None:
                    data = []

                return data

        except FileNotFoundError:

            print("NO ORDERBOOK FOUND. CREATING NEW FILE")

            with open(file_path, 'w') as x:
                json.dump([], x, indent=4)

            return []

        except json.JSONDecodeError:

            print("ORDERBOOK CORRUPTED. RESETTING")

            with open(file_path, 'w') as x:
                json.dump([], x, indent=4)

            return []
   

    
    def analyzing_the_data(self):
        main_data=self.opening_the_raw_file()
       
        orb_candle=[]
        master_closed_data=[]
        order_log=self.opening_the_order_log()

        
        for datas in main_data:
            current_close=datas['CLOSE']
            current_open=datas['OPEN']
            current_time=datas['TIME']
            current_date=datas['DATE']
            current_low=datas['LOW']
            current_high=datas['HIGH']
            master_closed_data.append(current_close)
            if current_date==self.latest_date:


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
                            if new_date==self.latest_date:
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
                        fourth_level_candle_retest_=None

                        


                        for retest_candle_ in main_data:
                            retest_candle_close=retest_candle_['CLOSE']
                            retest_candle_open=retest_candle_['OPEN']
                            retest_candle_date=retest_candle_['DATE']
                            retest_candle_high=retest_candle_['HIGH']
                            retest_candle_low=retest_candle_['LOW']
                            if current_date==retest_candle_date:
                                if retest_candle_close==original_closing_prices:

                                    if retest_candle_close>retest_candle_open:
                                        if retest_candle_open==orb_high and retest_candle_close>orb_high or retest_candle_close>orb_high and retest_candle_open>orb_high and retest_candle_low<orb_high or retest_candle_close>orb_high and retest_candle_open>orb_high and retest_candle_low==orb_high:

                                            fourth_level_candle_retest.append(retest_candle_)
                                           
                        if fourth_level_candle_retest:
                            for rtx in fourth_level_candle_retest:

                                timer=rtx['TIME']
                          
                            #return

                                                    
                       
                            for fourth_level_candle in main_data:
                                fourth_level_candle_close=fourth_level_candle['CLOSE']
                                fourth_level_candle_open=fourth_level_candle['OPEN']
                                fourth_level_candle_date=fourth_level_candle['DATE']
                                fourth_level_candle_time=fourth_level_candle['TIME']
                                fourth_level_candle_low=fourth_level_candle['LOW']
                                fourth_level_candle_high=fourth_level_candle['HIGH']
                                if current_date==fourth_level_candle_date:
                                        if fourth_level_candle_time<timer:
                                            

                                    
                                            if fourth_level_candle_close>fourth_level_candle_open:
                                                if fourth_level_candle_close>orb_high and fourth_level_candle_open<orb_high:
                                                    fourth_level_candle_breakout.append(fourth_level_candle)

                                                    only_candle=fourth_level_candle_breakout[-1]

                        else:
                            print('NOT A VALID SETUP')
                        

                        # if only_candle is not None:
                        #     print(only_candle)
                        fifth_level_candle_retest=[]
                        

                        for fifth_level_candle in main_data:
                            fifth_level_candle_close=fifth_level_candle['CLOSE']
                            fifth_level_candle_open=fifth_level_candle['OPEN']
                            fifth_level_candle_date=fifth_level_candle['DATE']
                            fifth_level_candle_time=fifth_level_candle['TIME']
                            fifth_level_candle_low=fifth_level_candle['LOW']
                            fifth_level_candle_high=fifth_level_candle['HIGH']
                            if current_date==fifth_level_candle_date:
                                if fifth_level_candle_close==original_closing_prices:

                                    if fifth_level_candle_close>fifth_level_candle_open:
                                        if fifth_level_candle_close>orb_low and fifth_level_candle_open>orb_low and fifth_level_candle_low<orb_low or fifth_level_candle_close>orb_low and fifth_level_candle_open==orb_low and fifth_level_candle_low<orb_low or fifth_level_candle_close>orb_low and fifth_level_candle_close>orb_low and fifth_level_candle_open>orb_low and fifth_level_candle_low==orb_low:
                                            fifth_level_candle_retest.append(fifth_level_candle)


                        print(fifth_level_candle_retest)
                        
                        if fifth_level_candle_retest:
                            for fifths in fifth_level_candle_retest:
                                
                                fif_time=fifths['TIME']

                                fifth_level_candle_breakout=[]
                                
                                for fif_breakout_candle in main_data:
                                    fit_close=fif_breakout_candle['CLOSE']
                                    fit_time=fif_breakout_candle['TIME']
                                    fif_date=fif_breakout_candle['DATE']
                                    fif_low=fif_breakout_candle['LOW']
                                    fif_high=fif_breakout_candle['HIGH']
                                    fit_open=fif_breakout_candle['OPEN']

                                    if current_date==fif_date:
                                        if fit_time<fif_time:
                                            if fit_close>fit_open:
                                                if fit_close>orb_low and fit_open<orb_low:
                                                    fifth_level_candle_breakout.append(fif_breakout_candle)

                                                    
                                                    fifth_level_candle_breakout.append(fif_breakout_candle)

                                                    final_fifth_value=fifth_level_candle_breakout[-1]

                                if final_fifth_value is not None:
                                    print(final_fifth_value)
                        else:
                            print('NOT A VALID SETUP')




    def bos_structure(self):
        main_data=self.opening_the_raw_file()
        closing_prices_set=[]
        highest_prices=[]
        main_testing_candle=[]

        for datas in main_data:
            close_datas=datas['CLOSE']
            open_datas=datas['OPEN']
            high_data=datas['HIGH'] 
            low_data=datas['LOW']
            date_data=datas['DATE']
            time_data=datas['TIME']
            if self.latest_date==date_data:
                closing_prices_set.append(close_datas)
        current_closing=closing_prices_set[-1]



        for current_data in main_data:
            current_closes=current_data['CLOSE']
            current_dates=current_data['DATE']
            if current_dates==self.latest_date:
                if current_closing==current_closes:
                    main_testing_candle.append(current_data)


        for curs in main_testing_candle: 
            cu_close=curs['CLOSE']
            cu_open=curs['OPEN']
            cu_date=curs['DATE']
        for laters in main_data:
            curren_dates=laters['DATE']
            curren_highs=laters['HIGH']
            if curren_dates==cu_date:
                highest_prices.append(curren_highs)
                 
                

        #print(highest_prices)
        most_high=max(highest_prices)
        # print(most_high)
        # print(current_closing)
        if current_closing>most_high:
            print('BOS DETECTED {}'.format(laters))


    def fvg_setups(self):
        main_data=self.opening_the_raw_file()
        master_close_data=[]
        master_timing_data=[]
        master_date_data=[]
        main_setup=[]
        fair_value_candle=[]
        current_close_set=[]
        recent_low_set=[]
        master_high_data=[]
        recent_time=[]
        order_log=self.opening_the_order_log()
        for recents in main_data:
            recent_datses=recents['DATE']
            recent_close=recents['CLOSE']
            recent_low=recents['LOW']
            times=recents['TIME']
            recent_low_set.append(recent_low)
            recent_time.append(times)


            current_close_set.append(recent_close)
        #print(current_close_set)
        current_price=current_close_set[-1]
        current_low=recent_low_set[-1]
        current_time_data=recent_time[-1]

        for orders in order_log:
            order_status=orders['STATUS']
            old_times=orders['TIME']
            if order_status=='OPEN':
                previous_candle_value=orders['PREVIOUS_CANDLE']
                if previous_candle_value<current_low:
                    if current_time_data>old_times:

                        print('FVG SETUP DETECTED')

                



        for datas in main_data:
            closing_prices=datas['CLOSE']
            opening_prices=datas['OPEN']
            timings=datas['TIME']
            high=datas['HIGH']
            low=datas['LOW']

            dates=datas['DATE']
            


            if self.latest_date==dates:
                master_close_data.append(closing_prices)
                master_timing_data.append(timings)
                master_date_data.append(dates)
                master_high_data.append(high)
                


        current_time=master_timing_data[-1]

        current_closing_price=master_close_data[-1]
        latest_date_=master_date_data[-1]

        for latest_datas in main_data:
            latest_close=latest_datas['CLOSE']
            latest_date=latest_datas['DATE']
            latest_opens=latest_datas['OPEN']
            latest_high=latest_datas['HIGH']
            latest_low=latest_datas['LOW']
            if latest_date_==self.latest_date:

                if current_closing_price==latest_close:
                    main_setup.append(latest_datas)
        print(main_setup)
        for mains in main_setup:
            main_close=mains['CLOSE']
            main_open=mains['OPEN']
            main_dates=mains['DATE']
            main_time=mains['TIME']
        revised_master_close_data=master_close_data[0:-1]
        revised_master_high_data=master_high_data[0:-1]

        max_close_value=max(revised_master_close_data)
        max_high_value=max(revised_master_high_data)

        if max_close_value>main_close and main_close>max_high_value:

            print('SETUP REJECTED')
            return

        elif max_close_value<main_close and max_high_value<main_close:

            fair_value_candle.append(main_close)


        previous_candle=master_close_data[-2]
        print(fair_value_candle)
        main_order_set=[]



        if fair_value_candle:
            for fairs in fair_value_candle:
                fair_close_price=fairs

                new_fair_order={
                    'CANDLE_1':fair_close_price,
                    'TIME':current_time,
                    'STATUS':'OPEN',
                    'PREVIOUS_CANDLE':previous_candle

                }
                order_log.append(new_fair_order)
            with open(r'C:\Users\dasho\fvg_orderbook','w') as hh:
                data=json.dump(order_log,hh,indent=4)
                return data


        
        
                










    
                
                        
                                                





                        





                                    



                        
                                            
                                    

                            





                

                            

                                

                    

            
o=ORB_CODE()
o.opening_the_order_log()
o.opening_the_raw_file()
o.analyzing_the_data()
o.bos_structure()
o.fvg_setups()
