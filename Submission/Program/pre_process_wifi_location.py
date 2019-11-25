# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 19:36:11 2019

@author: markm
"""
from os import walk
from datetime import datetime
import csv


def get_files(directory):
    for (dirpath, dirnames, filenames) in walk(directory):
        return filenames

def get_in_out(file):
    csvFile_in = open(file, "r")
    #csvFile_in = open("test.csv", "r")
    reader = csv.reader(csvFile_in)
    # 1 means in, 0 means out
    previous_flag = 0
    # previous_time preserve the time of last in or near
    previous_time = 0
    # in_time is used for recording in time(second)
    in_time = 0
    # near_time is used for recording near time(second)
    near_time = 0
    # curr_time
    curr_time = 0
    
    for item in reader:
        if reader.line_num == 1:
            continue
        
        curr_time = int(item[0])
        # initialize previous_flag and previous_time
        if reader.line_num == 2:
            previous_time = int(item[0])
            if item[1][0] == 'i':
                previous_flag = 1
            elif item[1][0] == 'n':
                previous_flag = 0
            continue
        # if the item is in building
        if item[1][0] == 'i':
            if previous_flag == 1:
                continue
            else:
                near_time += (int(item[0]) - previous_time)
                previous_flag = 1
                previous_time = int(item[0])
        # if near building    
        elif item[1][0] == 'n':
            if previous_flag == 1:
                in_time += (int(item[0]) - previous_time)
                previous_flag = 0
                previous_time = int(item[0])
            else:
                continue
        # else continue, to avoid noise
        else:
            continue
        
    csvFile_in.close()
    
    if previous_flag == 1:
        in_time += (curr_time - previous_time)
    else:
        near_time += (curr_time - previous_time)
        
    print("in_time:", in_time)
    print("near_time:", near_time)
    
    return [in_time, near_time]


def main():
    path = "wifi_location/"
    files = get_files("wifi_location")
    
    csvFile = open("wifi_location.csv", "w", newline='')
    writer = csv.writer(csvFile)
    writer.writerow(["uid", "in_time(second)", "near_time(second)", "in/all rate"])
    
    for file in files:
        file_name  = path + file
        result = get_in_out(file_name)
        writer.writerow([file[14:17], result[0], result[1], result[0]/(result[0]+result[1])])
    
    csvFile.close()
    
if __name__ == '__main__':
    main()
    
    
    
    