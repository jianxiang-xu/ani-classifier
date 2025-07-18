import numpy as np
import sklearn
import csv
with open(r"C:\Users\xujia\feature_vectors.txt", "r") as file: 
  data=np.array([list(map(int,line.strip().split(','))) for line in file])

# 计算出训练、交叉验证数据集的大小 
length = len(data) 
n_train= int(0.7*length) 
 # 抽取出训练、交叉验证、测试样本的下标 
idx = np.random.permutation(length) 
train_idx = idx[:n_train]
test_idx = idx[n_train:] 
# 根据下标直接抽取出训练数据集、交叉验证集 
train, test = data[train_idx], data[test_idx]
x_train,y_train=train[:,:128],train[:,-1]
x_test,y_test=test[:,:128],test[:,-1]

# 从 scikit-learn 中调用相应的预处理器 
from sklearn.preprocessing import OneHotEncoder 
enc = OneHotEncoder(handle_unknown='ignore') 
# 调用 fit_transform 来对输入数据做 OneHot Encoding 
x_train_one_hot = enc.fit_transform(x_train) 
# 由于上一步已经把所需的数据信息收集完毕 
# 所以这一步只需直接 transform 即可完成转化 
x_test_one_hot = enc.transform(x_test)

# 从 scikit-learn 中调用 MultinomialNB 
# from sklearn.naive_bayes import MultinomialNB  
# clf = MultinomialNB() 
# # 调用 fit 函数进行训练 
# clf.fit(x_train_one_hot, y_train) 
# # 调用 predict 函数进行预测，然后通过一些 numpy 运算输出模型的准确率 
# print(np.mean(y_test == clf.predict(x_test_one_hot)))
# from sklearn.tree import DecisionTreeClassifier  
# clf = DecisionTreeClassifier() 
# clf.fit(x_train, y_train) 
# print(np.mean(y_test == clf.predict(x_test))) 
from sklearn.svm import SVC  
clf = SVC() 
clf.fit(x_train, y_train) 
#print(np.mean(y_test == clf.predict(x_test))) 

with open(r"C:\Users\xujia\feature_vector_test.txt",'r')as f:
  data=f.read()
x_test1=np.array([list(map(int,data.strip().split(',')))])
print(clf.predict(x_test1))
