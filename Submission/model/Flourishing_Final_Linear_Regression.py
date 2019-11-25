# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 12:03:01 2019

@author: markm
"""

import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
#import seaborn as sns

df = pd.read_csv('train_final_post_sorted/features_and_flourishing_values_pre_label_all_add_missing_post_label_43(1).csv')

# delete useless columns
columns = ['Unnamed: 0', 'uid', 'pre_score', 'pre_label', 'post_label']
df.drop(columns, inplace=True, axis=1)

# use the first 30 samples as training set
X = df.iloc[:30, :27]
y = df.iloc[:30, 27:]

# change type to 'int'
y = y.astype('int')
# select best features
bestfeatures = SelectKBest(score_func=chi2, k=20)
fit = bestfeatures.fit(X,y)
dfscores = pd.DataFrame(fit.scores_)
dfcolumns = pd.DataFrame(X.columns)
#concat two dataframes for better visualization 
featureScores = pd.concat([dfcolumns,dfscores],axis=1)
featureScores.columns = ['Specs','Score']  #naming the dataframe columns
print(featureScores.nlargest(20,'Score'))  #print 10 best features

# sort by score and preserve feature names as list
new_featureScores = featureScores.sort_values('Score',ascending=False)
selected_KBest = new_featureScores['Specs'].tolist()

y = df.iloc[:30, 27:]
#get correlations of each features in dataset
corrmat = df.corr()

feature_corr = corrmat.iloc[27:, :]
feature_corr = feature_corr.T
feature_corr = feature_corr.sort_values('post_socre',ascending=True)

corr_list = feature_corr.index.tolist()

from sklearn.linear_model import LinearRegression
#from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn import metrics


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
    
#from sklearn.linear_model import Ridge

    
def cross_validation(f_list, X, y):
    scores = cross_val_score(LinearRegression(), X, y, cv=5)
    print(scores)
    print()
    
for i in range(1,21):
    f_list = corr_list[:i]
    print(f_list)
    train_get_score(f_list, X, y)
    
for i in range(1,21):
    f_list = selected_KBest[:i]
    print(f_list)
    train_get_score(f_list, X, y)
    
for i in range(1,21):
    f_list = selected_KBest[:i]
    print(f_list)
    Ridge_score(f_list, X, y)
    

f_list = ['phonelock_mean', 'phonelock_sum', 'conversation_sum', 'bluetooth_day_num']
X_train = df.iloc[:30, :27]
y_train = df.iloc[:30, 27:]

X_test = df.iloc[30:, :27]
y_test = df.iloc[30:, 27:]

lm = LinearRegression()
model = lm.fit(X_train[f_list], y_train)
predictions = lm.predict(X_test[f_list])
predictions
print("model_score：", model.score(X_test[f_list], y_test))
print("Mean Absolute Error", metrics.mean_absolute_error(y_test, predictions))
print("Mean Squared Error", metrics.mean_squared_error(y_test, predictions))
print("Root Mean Squared Error", np.sqrt(metrics.mean_squared_error(y_test, predictions)))
print(predictions)

predict_list = predictions.T.tolist()[0]

lable = []
for i in range(len(predict_list)):
    if predict_list[i] > 44:
        lable.append(1)
    else:
        lable.append(0)
    
actual_value = [0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1]

def evaluation_metrics(test,pred):
    auc_score = metrics.roc_auc_score(test,pred)
    logloss = metrics.log_loss(test,pred)
    accuracy = metrics.accuracy_score(test,pred)
    F_Measure = metrics.f1_score(test,pred)
    precision = metrics.precision_score(test,pred)
    recall = metrics.recall_score(test,pred)
    print('auc_score,logloss,accuracy,F_Measure,precision,recall')
    return [auc_score,logloss,accuracy,F_Measure,precision,recall]

print(evaluation_metrics(actual_value, lable))