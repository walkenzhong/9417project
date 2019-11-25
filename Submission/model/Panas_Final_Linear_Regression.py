# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 12:12:24 2019

@author: markm
"""

import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
#import seaborn as sns

df = pd.read_csv('train_final_post_sorted/features_and_panas_values_pre_label_all_add_missing_post_label_44(1).csv')

# delete useless columns
columns = ['Unnamed: 0', 'uid', 'pre_positive', 'pre_negative', 'pre_positive_label', 'post_positive_label', 'pre_negative_label', 'post_negative_label']
df.drop(columns, inplace=True, axis=1)

# use the first 30 samples as training set
X = df.iloc[:30, :27]
y_positive = df.iloc[:30, 27:28]
y_negative = df.iloc[:30, 28:29]

y_positive = y_positive.astype('int')
# select best features
bestfeatures = SelectKBest(score_func=chi2, k=20)
fit = bestfeatures.fit(X, y_positive)
dfscores = pd.DataFrame(fit.scores_)
dfcolumns = pd.DataFrame(X.columns)
#concat two dataframes for better visualization 
featureScores = pd.concat([dfcolumns,dfscores],axis=1)
featureScores.columns = ['Specs','positive_Score']  #naming the dataframe columns
print(featureScores.nlargest(20,'positive_Score'))  #print 10 best features
y_positive = df.iloc[:30, 27:28]

# sort by score and preserve feature names as list
new_featureScores = featureScores.sort_values('positive_Score',ascending=False)
selected_KBest_positive = new_featureScores['Specs'].tolist()
selected_KBest_positive

y_negative = y_negative.astype('int')
# select best features
bestfeatures = SelectKBest(score_func=chi2, k=20)
fit = bestfeatures.fit(X, y_negative)
dfscores = pd.DataFrame(fit.scores_)
dfcolumns = pd.DataFrame(X.columns)
#concat two dataframes for better visualization 
featureScores = pd.concat([dfcolumns,dfscores],axis=1)
featureScores.columns = ['Specs','negative_Score']  #naming the dataframe columns
print(featureScores.nlargest(20,'negative_Score'))  #print 10 best features
y_negative = df.iloc[:30, 28:29]

# sort by score and preserve feature names as list
new_featureScores = featureScores.sort_values('negative_Score',ascending=False)
selected_KBest_negative = new_featureScores['Specs'].tolist()

#get correlations of each features in dataset
corrmat = df.corr()

feature_corr_positive = corrmat.iloc[27:28, :]
feature_corr_positive = feature_corr_positive.T
feature_corr_positive = feature_corr_positive.sort_values('post_positive',ascending=True)

feature_corr_negative = corrmat.iloc[28:29, :]
feature_corr_negative = feature_corr_negative.T
feature_corr_negative = feature_corr_negative.sort_values('post_negative',ascending=True)

corr_list_positive = feature_corr_positive.index.tolist()
corr_list_negative = feature_corr_negative.index.tolist()

from sklearn.linear_model import LinearRegression
#from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn import metrics
#from sklearn.model_selection import cross_val_score, cross_val_predict

def train_get_score(f_list, X, y):
    X_train = X[f_list][:24]
    X_test = X[f_list][24:]
    y_train = y[:24]
    y_test = y[24:]
    lm = LinearRegression()
    model = lm.fit(X_train, y_train)
    predictions = lm.predict(X_test)
    print("model_score：", model.score(X_test, y_test))
    print("Mean Absolute Error", metrics.mean_absolute_error(y_test, predictions))
    print("Mean Squared Error", metrics.mean_squared_error(y_test, predictions))
    print("Root Mean Squared Error", np.sqrt(metrics.mean_squared_error(y_test, predictions)))
    print(lm.coef_)
    print()
    



f_list_positive = ['bluetooth_sum', 'bluetooth_mean', 'conversation_sum', 'conversation_day_num', 'bluetooth_day_num']
f_list_negative = ['phonecharge_sum', 'phonecharge_mean', 'dark_day_num']
X_train = df.iloc[:30, :27]

y_train_positive = df.iloc[:30, 27:28]
y_train_negative = df.iloc[:30, 28:29]

X_test = df.iloc[30:, :27]

y_test_positive = df.iloc[30:, 27:28]
y_test_negative = df.iloc[30:, 28:29]

def train_test(f_list, X_train, y_train, X_test, y_test):
    lm = LinearRegression()
    model = lm.fit(X_train[f_list], y_train)
    predictions = lm.predict(X_test[f_list])
    print("model_score：", model.score(X_test[f_list], y_test))
    print("Mean Absolute Error", metrics.mean_absolute_error(y_test, predictions))
    print("Mean Squared Error", metrics.mean_squared_error(y_test, predictions))
    print("Root Mean Squared Error", np.sqrt(metrics.mean_squared_error(y_test, predictions)))
    print(predictions.T.tolist())
    return predictions.T.tolist()[0]

prediction1 = train_test(f_list_positive, X_train, y_train_positive, X_test, y_test_positive)
prediction2 = train_test(f_list_negative, X_train, y_train_negative, X_test, y_test_negative)


lable_positive = []
lable_negative = []
for i in range(len(prediction2)):
    if prediction1[i] > 28:
        lable_positive.append(1)
    else:
        lable_positive.append(0)
    
    if prediction2[i] > 22:
        lable_negative.append(1)
    else:
        lable_negative.append(0)


def evaluation_metrics(test,pred):
    auc_score = metrics.roc_auc_score(test,pred)
    logloss = metrics.log_loss(test,pred)
    accuracy = metrics.accuracy_score(test,pred)
    F_Measure = metrics.f1_score(test,pred)
    precision = metrics.precision_score(test,pred)
    recall = metrics.recall_score(test,pred)
    print('auc_score,logloss,accuracy,F_Measure,precision,recall')
    return [auc_score,logloss,accuracy,F_Measure,precision,recall]

actual_positive = [1,1,0,1,1,0,0,0,1,0,1,1,0,1]
actual_negative = [0,1,0,1,0,1,0,1,0,1,0,1,1,1]

print(evaluation_metrics(actual_positive,lable_positive))
print(evaluation_metrics(actual_negative,lable_negative))