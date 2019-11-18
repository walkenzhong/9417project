import pandas as pd
import time
import numpy as np
import re
import os

#read all line from file, and return all line,not include header
def get_file(filename):
    all_file = pd.read_csv(filename,sep=',')
    return all_file

def from_timestamp_to_daytime(timestamp):
    return time.localtime(timestamp)

#get all filename in a dir
def get_filename(file_dir):
    for root,dirs,files in os.walk(file_dir):
        return files
def get_sum_and_var(daily_data):
    daily_mac_address_num = []
    for i in daily_data:
        daily_mac_address_num.append(i[3])
    return np.sum(daily_mac_address_num),np.var(daily_mac_address_num),np.mean(daily_mac_address_num),len(daily_mac_address_num)

def student_sum_and_var_and_mean(filename):
    all_data = get_file(filename)
    #print(all_data)
    data_and_mac_address = []
    for i in range(len(all_data)):
        time = from_timestamp_to_daytime(all_data['time'][i])
        year = time.tm_year
        mon = time.tm_mon
        day = time.tm_mday
        mac_address = all_data['MAC'][i]
        data_and_mac_address.append([year,mon,day,mac_address])
    #print(data_and_mac_address)
    start_year = data_and_mac_address[0][0]
    start_mon = data_and_mac_address[0][1]
    start_day = data_and_mac_address[0][2]
    mac_address_arr = []
    data_and_mac_address_num_daily = []
    for i in data_and_mac_address:
        end_year = i[0]
        end_mon = i[1]
        end_day = i[2]
        if(start_year == end_year and start_mon == end_mon and start_day == end_day):
            mac_address_arr.append(i[3])
        else:
            check_repeat = 1 # check mac address repeat, 1: check repeat, 0:not check repeat
            if check_repeat == 1:
                after_check_repeat_mac_address_arr = list(set(mac_address_arr))
            else:
                after_check_repeat_mac_address_arr = mac_address_arr
            mac_address_num = len(after_check_repeat_mac_address_arr)
            data_and_mac_address_num_daily.append([start_year,start_mon,start_day,mac_address_num])
            start_year = end_year
            start_mon = end_mon
            start_day = end_day
            mac_address_arr = []
            mac_address_arr.append(i[3])
    sum,var,mean,day_num = get_sum_and_var(data_and_mac_address_num_daily)
    student_uid = re.findall('bt_([^"]*).csv', filename)[0]
    return student_uid,sum,var,mean,day_num



def main(file_dir):
    all_filename = get_filename(file_dir)
    #print(all_filename)
    all_student_data = []
    for i in all_filename:
        student_uid,sum,var,mean,day_num = student_sum_and_var_and_mean(file_dir+i)
        print(student_uid)
        all_student_data.append([student_uid,sum,var,mean,day_num])
    return all_student_data


if __name__ == '__main__':
    all_student_data = main('..\\input\\sensor\\bluetooth\\')
    #np.savetxt('conversation.csv',all_student_data,delimiter = ',')
    name = ['uid','sum','var','mean','day_num']
    test = pd.DataFrame(columns=name,data=all_student_data)
    test.to_csv('data\\bluetooth.csv',encoding = 'gbk')
    print('done')