import pandas as pd
import time
import numpy as np
import re
import os

def get_file(filename):
    all_file = pd.read_csv(filename,sep=',')
    return all_file

def combine():
    flourishing = get_file('Flourishing_result.csv')
    panas= get_file('panas_result.csv')
    data = pd.merge(flourishing,panas)
    return data

def from_number_to_low_high():
    data = combine()
    for i in range(1,len(data.columns.values)):
        mean_num = np.mean(data[data.columns.values[i]])
        std_num = np.std(data[data.columns.values[i]],ddof=1)
        print(data.columns.values[i])
        for j in range(len(data[data.columns.values[i]])):
            now_num = (data[data.columns.values[i]][j] - mean_num)/std_num
            if now_num > 1:
                data[data.columns.values[i]][j] = 1
            elif now_num < -1:
                data[data.columns.values[i]][j] = -1
            else:
                data[data.columns.values[i]][j] = 0
    return data







if __name__ == '__main__':
    data = from_number_to_low_high()
    data.to_csv("output_label.csv",encoding = 'gbk')
