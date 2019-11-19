import pandas as pd

def gather_features(feature_files):
    # read all features into feature_list
    feature_list = []
    for file in feature_files:
        feature = pd.read_csv('data/' + file + '.csv')
        # remove first index column
        if file != 'wifi_location':
            feature = feature.iloc[:,1:]
        else:
            feature.columns = ['uid', 'in_time_second', 
                               'near_time_second', 'in_all_percentage']
        feature_list.append(feature)
        
    # join all feature on uid
    features = feature_list[0]
    for i in range(1, len(feature_list)):
        features = pd.merge(features, feature_list[i], on='uid', how='outer')
        
    # save all features to a csv file
    features.to_csv('data/all_features.csv')
    return features
    
feature_files = ['activity', 'audio', 'bluetooth', 'conversation', 'dark', 
    'phonecharge', 'phonelock', 'wifi_location']
features = gather_features(feature_files)