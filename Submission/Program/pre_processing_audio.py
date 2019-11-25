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
    audio_arr = []
    rows = len(csv)
    for i in range(len(csv)):
        timestamp = csv["timestamp"][i] - 18000
        timeArray = time.localtime(timestamp)
        audio_inference = csv[" audio inference"][i]
        if(audio_inference == 3):
            audio_inference = lastrecord
        lastrecord = audio_inference
        count += audio_inference
        sum += audio_inference
        nowday = timeArray.tm_mday
        if(nowday != lastday):
            audio_arr.append(count)
            day += 1
            count = 0
            lastday = nowday
    audio_arr.append(count)
    day += 1
    audio_mean = np.mean(audio_arr)
    audio_avg = sum/day
    audio_var = np.var(audio_arr)
    print(audio_mean, sum, rows, audio_avg, day, audio_var)
    return audio_mean, sum, rows, audio_avg, day, audio_var

#get all file names
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return(files)

def main():
    files = file_name("sensing/audio")
    path = "sensing/audio/"
    audio_mean = []
    audio_sum = []
    audio_rows = []
    audio_avg = []
    audio_var = []
    days = []
    student_id = []
    data = {}
    for file in files:
        filename = path + file
        uid = file[6:9]
        print(filename, uid)
        mean, sum, rows, avg, day, var = MeanAndSum(filename)
        audio_mean.append(mean)
        audio_sum.append(sum)
        audio_rows.append(rows)
        audio_avg.append(avg)
        audio_var.append(var)
        days.append(day)
        student_id.append(uid)
    data["uid"] = student_id
    data["audio_mean"] = audio_mean
    data["audio_sum"] = audio_sum
    data["audio_avg"] = audio_avg
    data["audio_var"] = audio_var
    data["day"] = days
    data["rows"] = audio_rows
    data_df = pd.DataFrame(data)
    data_df.to_csv("audio_1.8.csv")


if __name__ == '__main__':
    main()
