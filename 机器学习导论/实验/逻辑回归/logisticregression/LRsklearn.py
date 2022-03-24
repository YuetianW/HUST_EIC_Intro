from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import csv
from sklearn.preprocessing import StandardScaler

# 加载数据
df = pd.read_csv(r'钞票训练集.txt', header=None)
X_data = np.array(df.loc[:][[0, 1, 2, 3]])
y_data = df.loc[:][4].values

# 拆分测试集、训练集
X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.25, random_state=0)

# 标准化特征值（观察结果使准确度下降了0.3%，所以不再使用）
sc = StandardScaler()
sc.fit(X_train)
X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)

# 训练回归模型
logr = LogisticRegression()
logr.fit(X_train, y_train)
print("准确度:", logr.score(X_test, y_test))

# 预测
dpred = pd.read_csv(r'钞票测试集.txt', header=None)
X_pred = np.array(dpred.loc[:][[0, 1, 2, 3]])
y_pred = logr.predict(X_pred)
result = pd.DataFrame(X_pred)
result['result'] = y_pred
num = range(1, len(X_pred) + 1)
result.insert(loc=0, column='num', value=num)
# np.savetxt("result.csv", result, delimiter=",")
result.to_csv('result.csv', index=False, header=False)
