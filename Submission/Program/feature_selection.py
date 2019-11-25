from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
from sklearn import metrics
from sklearn.ensemble import ExtraTreesClassifier

import matplotlib.pyplot as plt

def get_file(filename):
    all_file = pd.read_csv(filename,sep=',')
    return all_file

def get_label(data):
    return data['post_socre']

def get_feature(data):
    feature = []
    for i in range(len(data['activity_mean'])):
        feature.append([data['activity_mean'][i],data['activity_var'][i],data['audio_mean'][i],data['audio_var'][i],data['bluetooth_sum'][i],data['bluetooth_var'][i],data['bluetooth_mean'][i],data['bluetooth_day_num'][i],data['conversation_sum'][i],data['conversation_var'][i],data['conversation_mean'][i],data['conversation_day_num'][i],data['dark_sum'][i],data['dark_var'][i],data['dark_mean'][i],data['dark_day_num'][i],data['phonecharge_sum'][i],data['phonecharge_var'][i],data['phonecharge_mean'][i],data['phonecharge_day_num'][i],data['phonelock_sum'][i],data['phonelock_var'][i],data['phonelock_mean'][i],data['phonelock_day_num'][i],data['in_time_second'][i],data['near_time_second'][i],data['in_all_percentage'][i],data['pre_score'][i]
])
    return feature

if __name__ == '__main__':
    filename = '..\\preprocess\\data\\features_and_flourishing.csv'
    all_data = get_file(filename)
    data_label = get_label(all_data)
    data_feature = get_feature(all_data)
    model = ExtraTreesClassifier()
    model.fit(data_feature,data_label)
    print(model.feature_importances_)
    j = 2
    label = []
    importance = []
    for i in model.feature_importances_:
        importance.append(i)
    for j in all_data.columns.values:
        label.append(j)
    print(label[2:len(model.feature_importances_)])
    print(importance)
    plt.bar(label[2:len(model.feature_importances_)+2],importance)
    plt.xticks(rotation=270)
    plt.gca().margins(x=0)
    plt.gcf().canvas.draw()
    tl = plt.gca().get_xticklabels()
    maxsize = max([t.get_window_extent().width for t in tl])
    m = 0.2  # inch margin
    s = maxsize / plt.gcf().dpi * 150 + 2 * m
    margin = m / plt.gcf().get_size_inches()[0]

    plt.gcf().subplots_adjust(left=margin, right=1. - margin)
    plt.gcf().set_size_inches(s, plt.gcf().get_size_inches()[1])
    plt.savefig('test.png',bbox_inches = 'tight')
    plt.show()
    j=0
    test= label[2:]
    for i in model.feature_importances_:
        print(test[j])
        print(i)
        j = j + 1
