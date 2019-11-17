import pandas as pd
import time
import numpy as np
import re
import os


# read all line from file, and return all line,not include header
def get_file(filename):
    all_file = pd.read_csv(filename, sep=',')
    return all_file

def get_filename(file_dir):
    for root,dirs,files in os.walk(file_dir):
        return files
# get time interval from each line
def get_time_interval(start_time, end_time):
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
    for i in range(len(time_and_interval) - 1):
        end_year = time_and_interval[i + 1][0]
        end_mon = time_and_interval[i + 1][1]
        end_day = time_and_interval[i + 1][2]
        if (start_year == end_year and start_mon == end_mon and start_day == end_day):
            day_interval_sum = day_interval_sum + time_and_interval[i][3]
        else:
            daily_data.append([start_year, start_mon, start_day, day_interval_sum])
            start_year = end_year
            start_mon = end_mon
            start_day = end_day
            day_interval_sum = 0
    return daily_data

def each_student_data(filename):
    file = get_file(filename)
    time_and_interval = []
    for i in range(len(file)):
        #print(from_timestamp_to_daytime(test['start_timestamp'][i]))
        time_interval = get_time_interval(file['start'][i],file['end'][i])
        daytime = from_timestamp_to_daytime(file['start'][i])
        year = daytime.tm_year
        #print(year)
        mon = daytime.tm_mon
        day = daytime.tm_mday
        time_and_interval.append([year,mon,day,time_interval])
    daily_data = get_daily_data(time_and_interval)
    student_uid = re.findall('phonelock_([^"]*).csv', filename)[0]
    return student_uid,daily_data

def main(file_dir):
    all_filename = get_filename(file_dir)
    for i in all_filename:
        student_uid,one_student_data = each_student_data(file_dir + i)
        name = ['year','mon','day','phonelock_time']
        student = pd.DataFrame(columns=name, data=one_student_data)
        file_in_paths = os.listdir("data20191117")
        #print(paths)
        if 'phonelock' not in file_in_paths :
            os.mkdir('data20191117\\phonelock\\')
        student.to_csv('data20191117\\phonelock\\phonelock_'+ student_uid + '.csv', encoding='gbk')
        print(student_uid)
    print('done')


if __name__ == '__main__':
    main('..\\input\\sensor\\phonelock\\')