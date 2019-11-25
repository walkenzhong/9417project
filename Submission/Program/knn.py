from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
from sklearn.model_selection import cross_val_score
import numpy as np
def get_file(filename):
    all_file = pd.read_csv(filename,sep=',')
    return all_file
def get_label(data):
    label = []
    for i in data['post_label']:
        label.append(i)
    return label
def get_feature(data,feature_name):
    feature = []
    for i in range(len(data['activity_mean'])):
        feature.append([data[feature_name][i]])
    return feature
def knn_cv_scores(input_feature,input_label,k):
    knn = KNeighborsClassifier(n_neighbors=k)
    label = []
    for i in input_label:
        label.append(i)
    cv_scores = cross_val_score(knn, input_feature, label, cv=3)
    print(cv_scores)
    return np.mean(cv_scores)
def knn_post_prediction(input_feature,input_label,predict_feature,true_predict_label,prediction_pre_score,k):
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(input_feature,input_label)
    predict_label = knn.predict(predict_feature)
    prediction_post_label = knn.predict(prediction_pre_score)
    knn_score = knn.score(predict_feature,true_predict_label)
    return predict_label,knn_score,prediction_post_label
def get_prediction_feature():
    filename = '..\\train_missing_post\\flourishing_missing_post.csv'
    all_data = get_file(filename)
    pre_score = []
    for i in all_data['pre_score']:
        pre_score.append([i])
    return pre_score
def main(filename):
    all_data = get_file(filename)
    all_feature_data = get_feature(all_data,'pre_score')
    all_label_data = get_label(all_data)
    train_feature_data = all_feature_data[:25]
    train_label_data = all_label_data[:25]
    test_feature_data = all_feature_data[25:]
    test_label_data = all_label_data[25:]
    print(train_feature_data)
    print(train_label_data)
    print(test_feature_data)
    print(test_label_data)
    prediction_pre_score = get_prediction_feature()
    for i in range(2,10):
        print(f'k = {i}')
        cv_scores = knn_cv_scores(train_feature_data,train_label_data,i)
        prediction_post,knn_score,prediction_post_label = knn_post_prediction(train_feature_data,train_label_data,test_feature_data,test_label_data,prediction_pre_score,i)
        print(f'cv_scores:{cv_scores},prediction_post:{prediction_post},knn_score:{knn_score}')
        print(f'final prediction:{prediction_post_label}')
if __name__ == '__main__':
    filename = '..\\train_missing_post\\features_and_flourishing_values_pre_label_all_no_missing_post_with_post_label.csv'
    main(filename)