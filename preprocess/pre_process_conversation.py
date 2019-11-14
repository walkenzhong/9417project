import pandas as pd
import time
import numpy as np
import re
import os

#read all line from file, and return all line,not include header
def get_file(filename):
    all_file = pd.read_csv(filename,sep=',')
    return all_file
    
#get time interval from each line
def get_time_interval(start_time,end_time):
    time_interval = end_time - start_time
    return time_interval
    
def from_timestamp_to_daytime(timestamp):
    return time.localtime(timestamp)

def get_daily_data(time_and_interval):
    start_year = time_and_interval[0][0]
    start_mon = time_and_interval[0][1]
    start_day = time_and_interval[0][2]
    day_interval_sum = 0
    daily_data = []
    for i in range(len(time_and_interval)-1):
        end_year = time_and_interval[i+1][0]
        end_mon = time_and_interval[i+1][1]
        end_day = time_and_interval[i+1][2]
        if(start_year == end_year and start_mon == end_mon and start_day == end_day):
            day_interval_sum = day_interval_sum + time_and_interval[i][3]
        else:
            daily_data.append([start_year,start_mon,start_day,day_interval_sum])
            start_year = end_year
            start_mon = end_mon
            start_day = end_day
            day_interval_sum = 0
    return daily_data
def get_interval_sum_and_var(daily_data):
    daily_interval = []
    for i in daily_data:
        daily_interval.append(i[3])
        #print(i[3])
    #print(daily_interval)
    return np.sum(daily_interval),np.var(daily_interval)
    
def student_sum_and_var(filename):
    file = get_file(filename)
    time_and_interval = []
    for i in range(len(file)):
        #print(from_timestamp_to_daytime(test['start_timestamp'][i]))
        time_interval = get_time_interval(file['start_timestamp'][i],file[' end_timestamp'][i])
        daytime = from_timestamp_to_daytime(file['start_timestamp'][i])
        year = daytime.tm_year
        #print(year)
        mon = daytime.tm_mon
        day = daytime.tm_mday
        time_and_interval.append([year,mon,day,time_interval])
    daily_data = get_daily_data(time_and_interval)
    sum,var = get_interval_sum_and_var(daily_data)
    student_uid = re.findall('conversation_([^"]*).csv', filename)[0]
    return student_uid,sum,var
    
def get_filename(file_dir):
    for root,dirs,files in os.walk(file_dir):
        return files
        
def main(file_dir):
    all_filename = get_filename(file_dir)
    print(all_filename)
    all_student_data = []
    for i in all_filename:
        student_uid,sum,var = student_sum_and_var(file_dir+i)
        print(student_uid)
        all_student_data.append([student_uid,sum,var])
    return all_student_data
if __name__ == '__main__':
    all_student_data = main('..\\input\\sensor\\conversation\\')
    #np.savetxt('conversation.csv',all_student_data,delimiter = ',')
    name = ['uid','sum','var']
    test = pd.DataFrame(columns=name,data=all_student_data)
    test.to_csv('data\\conversation.csv',encoding = 'gbk')
    print('done')
    #print(student_sum_and_var())

        