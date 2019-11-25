# pre-processing of FlourishingScale.csv
# Input: FlourishingScale.csv
# Output: Flourishing.csv
#         uid, FlourishingScale_value

import numpy as np
import csv
from sklearn.preprocessing import Imputer
# the flag for missing value imputation later


def main(missing_mode):
    
    csvFile = open("FlourishingScale.csv", "r")
    reader = csv.reader(csvFile)
    
    result_pre = list()
    result_post = list()
    
    dic_pre = dict()
    dic_post = dict()
    dic_final = dict()
    
    for item in reader:
        if reader.line_num == 1:
            continue
        if item[1] == "pre":
            result_pre.append(item)
        elif item[1] == "post":
            result_post.append(item)
    
    for u in result_pre:
        for i in range(2,10):
            if u[i] == '':
                u[i] = 0
            else:
                u[i] = int(u[i])
    
    for u in result_post:
        for i in range(2,10):
            if u[i] == '':
                u[i] = 0
            else:
                u[i] = int(u[i])   
        
          
    result_pre2 = np.asarray(result_pre)
    user_pre = result_pre2[:, :1]
    result_pre2 = np.delete(result_pre2, np.s_[:2], axis=1)
    
    result_post2 = np.asanyarray(result_post)
    user_post = result_post2[:, :1]
    result_post2 = np.delete(result_post2, np.s_[:2], axis=1)
    
    
    imp = Imputer(missing_values=0, strategy= missing_mode)
    result_pre3 = imp.fit_transform(result_pre2)
    result_post3 = imp.fit_transform(result_post2)
    
    
    for i in range(len(user_pre)):
        dic_pre[user_pre[i].item()] = result_pre3[i].sum().item()
    
    for i in range(len(user_post)):
        dic_post[user_post[i].item()] = result_post3[i].sum().item()
        
    
    user = list()
    
    for i in dic_pre:
        user.append(i)
    for i in dic_post:
        if i in user:
            pass
        else:
            user.append(i)
            
        
    ######################################
    
    for u in user:
        if u in dic_pre:
            if u in dic_post:
                dic_final[u] = 0.5*(dic_pre[u]+dic_post[u])
            else:
                dic_final[u] = dic_pre[u]
        else:
            if u in dic_post:
                dic_final[u] = dic_post[u]
    
    
    csvFile = open("Flourishing_result.csv", "w", newline='')
    writer = csv.writer(csvFile)
    writer.writerow(["uid", "pre_score", "post_socre", "Flourishing_score"])
    for key in sorted(dic_final):
        pre_score = 0
        post_score = 0
        if key in dic_pre:
            pre_score = dic_pre[key]
        if key in dic_post:
            post_score = dic_post[key]
            
        writer.writerow([key, pre_score, post_score, dic_final[key]])
    
    csvFile.close()


if __name__ == '__main__':
    # parameter can be "median", "mean", "most_frequent"
    main("median")