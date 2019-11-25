import pandas as pd
import time
import numpy as np
import re
import os

def get_file(filename):
    all_file = pd.read_csv(filename,sep=',')
    return all_file

def combine():
    flourishing = get_file('..\\train_missing_post\\features_and_panas_values_pre_label_all_no_missing_post.csv')
    #panas= get_file('panas_result_without0.csv')
    #data = pd.merge(flourishing,panas)
    return flourishing

def from_number_to_low_high():
    data = combine()
    print(data.columns.values[-2:-1])
    mean_num = np.mean(data['post_positive_label'])
    #print(mean_num)
    #print(data['pre_label'][48])
    std_num = np.std(data['post_positive_label'])
    for i in range(len(data['post_positive_label'])):
        now_num = (data['post_positive_label'][i] - mean_num)/std_num
        if now_num < -1:
            data['post_positive_label'][i] = 0
        else:
            data['post_positive_label'][i] = 1
    mean_num = np.mean(data['post_negative_label'])
    #print(mean_num)
    #print(data['pre_label'][48])
    std_num = np.std(data['post_negative_label'])
    for i in range(len(data['post_negative_label'])):
        now_num = (data['post_negative_label'][i] - mean_num)/std_num
        if now_num < -1:
            data['post_negative_label'][i] = 0
        else:
            data['post_negative_label'][i] = 1
    return data





if __name__ == '__main__':
    data = from_number_to_low_high()
    data.to_csv("features_and_panas_values_pre_label_all_no_missing_post_with_post_label.csv",encoding = 'gbk')
