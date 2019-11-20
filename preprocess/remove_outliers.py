import pandas as pd
from sklearn.ensemble import IsolationForest

def get_line(data):
    min_num = min(data)
    max_num = max(data)
    new_data = []
    for i in data:
        new_one = (max_num - i)/(max_num - min_num)
        new_data.append(new_one)
    return new_data

def normalization(all_data):
    #print(all_data.columns.values)
    for i in range(1,len(all_data.columns.values)):
        #print(all_data.columns.values[i])
        all_data[all_data.columns.values[i]] = get_line(all_data[all_data.columns.values[i]])
    all_data.to_csv("data/all_features_normalised.csv")

def remove_outliers(all_features):
    # remove uid column for training 
    features_without_uid = all_features.iloc[:,1:]

    # Use isolation forest to detect outliers

    # training the model
    # contamination: percentage of outliers
    # max_samples: # of samples to draw from X to train each base estimator.
    # max_samples: default = all samples
    clf = IsolationForest(contamination=0.1, behaviour='new')
    clf.fit(features_without_uid)

    # predictions
    pred_outliers = clf.predict(features_without_uid)
    outlier_rows = []
    for i in range(len(pred_outliers)):
        if (pred_outliers[i] == -1):
            # print outliers
            print(all_features['uid'][i])
            outlier_rows.append(i)

    # remove the row containing outliers
    all_features_without_outliers = all_features.drop(outlier_rows)
    all_features_without_outliers.to_csv("data/all_features_without_outliers.csv")
    return all_features_without_outliers
    
    
def main():
    all_features = pd.read_csv('data/all_features.csv')
    # remove first index column
    all_features = all_features.iloc[:,1:]
    
    # fill NaN value with 0
    # NaN found at index 31:
    # 	student: u39 
    #   col: phonecharge_var, phonecharge_mean
    all_features = all_features.fillna(0)
    
    # get rid of outliers
    all_features_without_outliers = remove_outliers(all_features)

    # normalise features and save to csv
    normalization(all_features_without_outliers)


if __name__ == '__main__':
    main()
