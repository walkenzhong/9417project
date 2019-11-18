import pandas as pd
import time
import numpy as np
import re
import os
import matplotlib.pyplot as plt

#get data from file
def get_file(filename):
    all_file = pd.read_csv(filename,sep=',')
    return all_file

def from_timestamp_to_daytime(timestamp):
    return time.localtime(timestamp)

#get all filename in a dir
def get_filename(file_dir):
    for root,dirs,files in os.walk(file_dir):
        return files

def each_student_data(filename):
    all_data = get_file(filename)
    # print(all_data)
    data_and_mac_address = []
    for i in range(len(all_data)):
        time = from_timestamp_to_daytime(all_data['time'][i])
        year = time.tm_year
        mon = time.tm_mon
        day = time.tm_mday
        mac_address = all_data['MAC'][i]
        data_and_mac_address.append([year, mon, day, mac_address])
    # print(data_and_mac_address)
    start_year = data_and_mac_address[0][0]
    start_mon = data_and_mac_address[0][1]
    start_day = data_and_mac_address[0][2]
    mac_address_arr = []
    data_and_mac_address_num_daily = []
    for i in data_and_mac_address:
        end_year = i[0]
        end_mon = i[1]
        end_day = i[2]
        if (start_year == end_year and start_mon == end_mon and start_day == end_day):
            mac_address_arr.append(i[3])
        else:
            check_repeat = 1  # check mac address repeat, 1: check repeat, 0:not check repeat
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
    student_uid = re.findall('bt_([^"]*).csv', filename)[0]
    return student_uid,data_and_mac_address_num_daily

def main(file_dir):
    all_filename = get_filename(file_dir)
    for i in all_filename:
        student_uid,one_student_data = each_student_data(file_dir + i)
        name = ['year','mon','day','mac_address_num']
        student = pd.DataFrame(columns=name, data=one_student_data)
        show_plt(student_uid,one_student_data)
        file_in_paths = os.listdir("data20191117")
        #print(paths)
        if 'bluetooth' not in file_in_paths :
            os.mkdir('data20191117\\bluetooth\\')
        student.to_csv('data20191117\\bluetooth\\bluetooth_'+ student_uid + '.csv', encoding='gbk')
        print(student_uid)
    print('done')

def show_plt(uid,student):
    time = []
    data = []
    for i in student:
        time_str = str(i[1]) + '.' + str(i[2])
        time.append(time_str)
        data.append(i[3])
    plt.xticks(rotation=270)
    plt.bar(time, data)
    plt.gca().margins(x=0)
    plt.gcf().canvas.draw()
    tl = plt.gca().get_xticklabels()
    maxsize = max([t.get_window_extent().width for t in tl])
    m = 0.2  # inch margin
    s = maxsize / plt.gcf().dpi * 150 + 2 * m
    margin = m / plt.gcf().get_size_inches()[0]

    plt.gcf().subplots_adjust(left=margin, right=1. - margin)
    plt.gcf().set_size_inches(s, plt.gcf().get_size_inches()[1])
    plt.savefig('data20191117\\bluetooth\\bluetooth_' + uid +".png")
    plt.show()




if __name__ == '__main__':
    main('..\\input\\sensor\\bluetooth\\');