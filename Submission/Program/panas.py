# pre-processing of panas.csv
# Input: panas.csv
# Output: 

import numpy as np
import csv
from sklearn.preprocessing import Imputer


def main(missing_mode):
    
    csvFile = open("panas.csv", "r")
    reader = csv.reader(csvFile)
    
    result_pre = list()
    result_post = list()
    
    pre_positive = dict()
    pre_negative = dict()
    post_positive = dict()
    post_negative = dict()
    
    dic_positive = dict()
    dic_negative = dict()
    
    for item in reader:
        if reader.line_num == 1:
            continue
        if item[1] == "pre":
            result_pre.append(item)
        elif item[1] == "post":
            result_post.append(item)
    
    
    
    for u in result_pre:
        for i in range(2,20):
            if u[i] == '':
                u[i] = 0
            else:
                u[i] = int(u[i])
    
    for u in result_post:
        for i in range(2,20):
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
    
    
    
    positive = [0,3,7,8,10,11,13,14,16]
    negative = [1,2,4,5,6,9,12,15,17]
    
    for i in range(len(user_pre)):
        p_score = 0
        n_score = 0
        for j in range(18):
            if j in positive:
                p_score += int(result_pre3[i][j].item())
            else:
                n_score += int(result_pre3[i][j].item())
        
        pre_positive[user_pre[i].item()] = p_score
        pre_negative[user_pre[i].item()] = n_score
    
    print(len(pre_positive))  
    #print(pre_negative)
    
    for i in range(len(user_post)):
        p_score = 0
        n_score = 0
        for j in range(18):
            if j in positive:
                p_score += int(result_post3[i][j].item())
            else:
                n_score += int(result_post3[i][j].item())
        
        post_positive[user_post[i].item()] = p_score
        post_negative[user_post[i].item()] = n_score
    
    print(len(post_positive))  
    #print(post_negative)
    
    user = list()
    
    for i in pre_positive:
        user.append(i)
    for i in post_positive:
        if i in user:
            pass
        else:
            user.append(i)
            
    user.sort()
    
    
    for u in user:
        if u in pre_positive:
            if u in post_positive:
                dic_positive[u] = 0.5*(pre_positive[u]+post_positive[u])
                dic_negative[u] = 0.5*(pre_negative[u]+post_negative[u])
            else:
                dic_positive[u] = pre_positive[u]
                dic_negative[u] = pre_negative[u]
        else:
            if u in post_positive:
                dic_positive[u] = post_positive[u]
                dic_negative[u] = post_negative[u]
    

    
    csvFile2 = open("panas_result.csv", "w", newline='')
    writer = csv.writer(csvFile2)
    writer.writerow(["uid", "pre_positive", "post_positive", "positive", "pre_negative", "post_negative","negative"])
    
    for key in sorted(dic_positive):
#    for key in sorted(user):
        pre_pos = 0
        post_pos = 0
        pre_neg = 0
        post_neg = 0
        if key in pre_positive:
            pre_pos = pre_positive[key]
        if key in post_positive:
            post_pos = post_positive[key]
        if key in pre_negative:
            pre_neg = pre_negative[key]
        if key in post_negative:
            post_neg = post_negative[key]
            
        writer.writerow([key, pre_pos, post_pos, dic_positive[key], pre_neg, post_neg, dic_negative[key]])
#        writer.writerow([key, pre_pos, post_pos, 0.5*(pre_pos + post_pos), pre_neg, post_neg, 0.5*(pre_neg + post_neg)])
    
    csvFile2.close()
    csvFile.close()


if __name__ == '__main__':
    # parameter can be "median", "mean", "most_frequent"
    main("median")