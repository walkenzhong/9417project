## comp9417 project
preprocess为处理好的数据及处理的代码  
input里为原始的sensor数据，但是太大了不给上传  
*** 
### data
#### bluetooth.csv  
uid: student id  
sum: 接触过的蓝牙设备数量总和（去除每日重复）  
var: 每日接触蓝牙设备数量的方差
#### conversation.csv
uid: student id  
sum: 通话时间总和   
var: 每日通话时间的方差  
#### dark.csv
uid: student id  
sum: 处于黑暗时间的总和  
var: 每日处于黑暗时间的方差  
#### phonecharge.csv
uid: student id  
sum: 充电时间总和  
var: 每日充电时间的方差  
#### phonelock.csv
uid: student id  
sum: 解锁时间总和  
var: 每日解锁时间的方差  

### data20191117
更新预处理，结果为统计每天时间，并输出每个学生每天的时间及日期到单独的一张csv表上,数据可视化已完成  
均值及天数更新在data的csv中

### normalization
data中的normalization.csv为所有feature归一化后的值