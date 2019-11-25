from itertools import combinations
import pandas as pd
from sklearn.model_selection import cross_val_score, GridSearchCV
import numpy
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier

#show future importance
def Getplt(name, value):
    fig, ax = plt.subplots()
    b = ax.barh(range(len(name)), value)
    for rect in b:
        w = rect.get_width()
        ax.text(w, rect.get_y() + rect.get_height() / 2, '%lf' % w, ha='left', va='center')
    ax.set_yticks(range(len(name)))
    ax.set_yticklabels(name)
    plt.show()

#inputfile
sensing = pd.read_csv("train_final_post/features_and_panas_values_pre_label_all_add_missing_post_label_44.csv")
#sensing = pd.read_csv("train_final_post/features_and_flourishing_values_pre_label_all_add_missing_post_label_43.csv")
features = ['activity_mean', 'activity_var', 'audio_mean', 'audio_var',
                'bluetooth_var', 'bluetooth_mean','conversation_var', 'conversation_mean',
                'dark_var', 'dark_mean','phonecharge_var', 'phonecharge_mean',
                'phonelock_var', 'phonelock_mean', 'in_all_percentage',]
y_name = "post_negative_label"
#y_name = "post_label"

#use combinations to get better oob scores
def GetBestFeature(new_features, number):
    best_features = []
    best_oob = 0.5
    for features in list(combinations(new_features, number)):
        #print(features)
        features = list(features)
        X = sensing[features]
        Xtrain = X[:30]
        Xtest = X[30:]
        le = LabelEncoder()
        le.fit(sensing[y_name])
        y = le.transform(sensing[y_name])
        ytrain = y[:30]
        ytest = y[30:]
        # 1.defult：
        rf0 = RandomForestClassifier(oob_score=True, random_state=8)
        rf0.fit(Xtrain, ytrain)
        y_predprob = rf0.predict_proba(Xtest)[:, 1]
        acc_score = cross_val_score(rf0, Xtrain, ytrain, cv=3, scoring='accuracy')
        #print("AUC Score : %f" % metrics.roc_auc_score(ytest, y_predprob))
        #print("oob_score:", rf0.oob_score_)
        if (rf0.oob_score_ > best_oob and metrics.roc_auc_score(ytest, y_predprob) > 0.6 and numpy.max(acc_score) - numpy.min(auc_score) < 0.2):
            best_oob = rf0.oob_score_
            best_features = features
    return best_features, best_oob

#use defult parameter to get scores
def MetricsDefult(features):
    X = sensing[features]
    Xtrain = X[:30]
    Xtest = X[30:]
    le = LabelEncoder()
    le.fit(sensing[y_name])
    y = le.transform(sensing[y_name])
    ytrain = y[:30]
    ytest = y[30:]
    rf0 = RandomForestClassifier(oob_score=True, random_state=8)
    rf0.fit(Xtrain, ytrain)
    print("oob_score:", rf0.oob_score_)
    y_predprob = rf0.predict_proba(Xtest)[:, 1]
    ypred = rf0.predict(Xtest)
    acc_score = cross_val_score(rf0, Xtrain, ytrain, cv=3, scoring='accuracy')
    accuracy = metrics.accuracy_score(ytest, ypred)
    F_Measure = metrics.f1_score(ytest, ypred)
    precision = metrics.precision_score(ytest, ypred)
    recall = metrics.recall_score(ytest, ypred)
    print("acc(train) :", acc_score)
    print("average acc:", numpy.mean(acc_score))
    print("AUC Score : %f" % metrics.roc_auc_score(ytest, y_predprob))
    print('precision ratio: %.2f%%' % (100 * precision))
    print('Recall ratio: %.2f%%' % (100 * recall))
    print('Accuracy ratio: %.2f%%' % (100 * accuracy))
    print('F-Measure ratio: %.2f%%' % (100 * F_Measure))
    Getplt(features, rf0.feature_importances_)

#use the specific parameters
def MetricsAfterTune(features, n_estimators):
    X = sensing[features]
    Xtrain = X[:30]
    Xtest = X[30:]
    le = LabelEncoder()
    le.fit(sensing[y_name])
    y = le.transform(sensing[y_name])
    ytrain = y[:30]
    ytest = y[30:]
    rf0 = RandomForestClassifier(n_estimators = n_estimators,max_features=2, oob_score=True, random_state=8)
    rf0.fit(Xtrain, ytrain)
    print("oob_score:", rf0.oob_score_)
    y_predprob = rf0.predict_proba(Xtest)[:, 1]
    ypred = rf0.predict(Xtest)
    auc_score = cross_val_score(rf0, Xtrain, ytrain, cv=3, scoring='accuracy')
    accuracy = metrics.accuracy_score(ytest, ypred)
    F_Measure = metrics.f1_score(ytest, ypred)
    precision = metrics.precision_score(ytest, ypred)
    recall = metrics.recall_score(ytest, ypred)
    print("auc(train) :", auc_score)
    print("average auc:", numpy.mean(auc_score))
    print("AUC Score : %f" % metrics.roc_auc_score(ytest, y_predprob))
    print('precision ratio: %.2f%%' % (100 * precision))
    print('Recall ratio: %.2f%%' % (100 * recall))
    print('Accuracy ratio: %.2f%%' % (100 * accuracy))
    print('F-Measure ratio: %.2f%%' % (100 * F_Measure))

#gridsearch n_estimators and max_features
def TuneParameter(features, n_estimators ):
    X = sensing[features]
    Xtrain = X[:30]
    le = LabelEncoder()
    le.fit(sensing[y_name])
    y = le.transform(sensing[y_name])
    ytrain = y[:30]
    param_test1 = {'n_estimators': n_estimators, 'max_features':[2,4,6,8]}
    gsearch1 = GridSearchCV(estimator=RandomForestClassifier(random_state=8),
                            param_grid=param_test1, scoring='accuracy', cv=3)
    gsearch1.fit(Xtrain, ytrain)
    print(gsearch1.best_params_, gsearch1.best_score_)

def main():
    #new_features, oob = GetBestFeature(features,2)
    #print(new_features)
    new_features =  ['activity_mean', 'audio_mean', 'audio_var', 'bluetooth_var', 'conversation_var', 'dark_mean', 'phonelock_var', 'phonelock_mean', 'in_all_percentage']
    MetricsDefult(new_features)
    n_estimators = []
    for i in range(50, 150):
        n_estimators.append(i)
    #TuneParameter(new_features, n_estimators)
    MetricsAfterTune(new_features,106)

if __name__ == '__main__':
    main()
