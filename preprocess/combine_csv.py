import pandas as pd

activity = pd.read_csv('data\\activity_1.6.csv')
audio = pd.read_csv('data\\activity_1.6.csv')
bluetooth = pd.read_csv('data\\bluetooth.csv')
conversation = pd.read_csv('data\\conversation.csv')
dark = pd.read_csv('data\\dark.csv')
phonecharge = pd.read_csv('data\\phonecharge.csv')
phonelock = pd.read_csv('data\\phonelock.csv')



data = pd.merge(activity, audio,bluetooth,conversation,dark,phonecharge,phonelock)  # pandas csv表左连接
data = data[['uid','activity_mean','activity_sum','activity_avg','rows','day','audio_mean','audio_sum','audio_avg','day','rows','bluetooth_sum','bluetooth_var','bluetooth_mean','bluetooth_day_num','conversation_sum','conversation_var','conversation_mean','conversation_day_num','dark_sum','dark_var','dark_mean','dark_day_num','phonecharge_sum','phonecharge_var','phonecharge_mean','phonecharge_day_num','phonelock_sum','phonelock_var','phonelock_mean','phonelock_day_num']]

data.to_csv(r'data.csv', encoding='gbk')
