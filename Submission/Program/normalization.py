import pandas as pd
import time
import numpy as np
import re
import os

def get_line(data):
    min_num = min(data)
    max_num = max(data)
    new_data = []
    for i in data:
        new_one = (max_num - i)/(max_num - min_num)
        new_data.append(new_one)
    return new_data

def normalization(filename):
    all_data = pd.read_csv(filename, sep=',')
    #print(all_data.columns.values)
    for i in range(2,len(all_data.columns.values)):
        print(all_data.columns.values[i])
        all_data[all_data.columns.values[i]] = get_line(all_data[all_data.columns.values[i]])
    all_data.to_csv("data\\normalization.csv",encoding = 'gbk')


if __name__ == '__main__':
    normalization("data\\all_features.csv")