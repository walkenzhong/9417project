import pandas as pd
import time, datetime
import numpy as np
import os

#get mean and sum and var
def MeanAndSum(filename):
    count = 0
    sum = 0
    csv = pd.read_csv(filename)
    lastday = time.localtime(csv["timestamp"][0] - 18000).tm_mday
    day = 0
    lastrecord = 0
    activity_arr = []
    rows = len(csv)
    for i in range(len(csv)):
        timestamp = csv["timestamp"][i] - 18000
        timeArray = time.localtime(timestamp)
        activity_inference = csv[" activity inference"][i]
        if(activity_inference == 3):
            activity_inference = lastrecord
        lastrecord = activity_inference
        count += activity_inference
        sum += activity_inference
        nowday = timeArray.tm_mday
        if(nowday != lastday):
            activity_arr.append(count)
            day += 1
            count = 0
            lastday = nowday
    activity_arr.append(count)
    day += 1
    activity_mean = np.mean(activity_arr)
    activity_var = np.var(activity_arr)
    avg = sum/day
    print(activity_mean, sum, rows, day, avg, activity_var, len(activity_arr))
    return activity_mean, sum, rows, day, avg, activity_var, len(activity_arr)

#get all file names
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return(files)

def main():
    files = file_name("sensing/activity")
    path = "sensing/activity/"
    activity_mean = []
    activity_sum = []
    activity_rows = []
    student_id = []
    activity_day = []
    activity_avg = []
    activity_var = []
    lengths = []
    data = {}
    for file in files:
        filename = path + file
        uid = file[9:12]
        print(filename, uid)
        mean, sum, rows, day, avg, var, length = MeanAndSum(filename)
        activity_mean.append(mean)
        activity_sum.append(sum)
        activity_rows.append(rows)
        activity_day.append(day)
        activity_avg.append(avg)
        student_id.append(uid)
        activity_var.append(var)
        lengths.append(length)
    data["uid"] = student_id
    data["activity_mean"] = activity_mean
    data["activity_sum"] = activity_sum
    data["activity_avg"] = activity_avg
    data["activity_var"] = activity_var
    data["rows"] = activity_rows
    data["day"] = activity_day
    data["length"] = lengths
    data_df = pd.DataFrame(data)
    data_df.to_csv("activity_1.8.csv")


if __name__ == '__main__':
    main()
