import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.impute import SimpleImputer as Imputer  # 引入skleran的数据填充方法；
from sklearn.metrics import accuracy_score

# 预处理
Train_data_f = pd.read_csv('DataSetKMeans1.csv',encoding='gbk')
Test_data_f = pd.read_csv('DataSetKMeans2.csv',encoding='gbk')
imputer = Imputer(missing_values=np.nan, strategy='constant', fill_value=-100)
Train_data = pd.DataFrame(imputer.fit_transform(Train_data_f))
Test_data = pd.DataFrame(imputer.fit_transform(Test_data_f))
Train_data.columns = Train_data_f.columns
Test_data.columns = Test_data_f.columns
feature_train = Train_data_f[['finLabel', 'BSSIDLabel', 'RoomLabel']]
feature_test = Test_data_f[['finLabel', 'BSSIDLabel', 'RoomLabel']]

BSSID_v = list(set(Train_data_f['BSSIDLabel']))
BSSID_l = len(BSSID_v)
tarin_bssid = feature_train.groupby('finLabel')
tarin_input = []
Train_data_classes = []
for i, v in tarin_bssid:
    tmp = np.array(v['BSSIDLabel'])
    tmpa = BSSID_l * [0]
    for bssidv in BSSID_v:
        if bssidv in tmp:
            tmpa[BSSID_v.index(bssidv)] = 1
    tarin_input.append(tmpa)
    roomid = np.array(v['RoomLabel'])
    Train_data_classes.append(roomid[1])



test_bssid = feature_test.groupby('finLabel')
test_input = []
Test_data_classes = []
for i, v in test_bssid:
    tmp1 = np.array(v['BSSIDLabel'])
    tmpa1 = BSSID_l * [0]
    for bssidv in BSSID_v:
        if bssidv in tmp1:
            tmpa1[BSSID_v.index(bssidv)] = 1
    test_input.append(tmpa1)
    roomid1 = np.array(v['RoomLabel'])
    Test_data_classes.append(roomid1[1])
Test_data_inputs = np.array(test_input)
#
# # 建立决策树  在此全部为默认参数了  主要参数criterion可选‘gini'或'entropy'作为生成树依据,max_deoth可以决定树的深度，max_leaf_nodes限制最大叶子树
# decision_tree_classifier = DecisionTreeClassifier()
# decision_tree_classifier.fit(tarin_input, Train_data_classes)
# decision_tree_output = decision_tree_classifier.predict(Test_data_inputs)
#
# print('真实值是：')
# print(Test_data_classes)
#
# print('预测值是:')
# print(decision_tree_output)
# score = accuracy_score(Test_data_classes, decision_tree_output)
# print(score)

# Train_data_classes = Train_data['RoomLabel'].values


# 先用 pandas 对每行生成字典，然后进行向量化
# vec=DictVectorizer(sparse=False)
# feature_train = Train_data[['BSSIDLabel', 'RSSLabel', 'SSIDLabel', 'finLabel']]
# Train_data_inputs_f = pd.get_dummies(feature_train)
#
# BSSID = set(feature_train['BSSIDLabel'])
#
# # Train_data_inputs = vec.fit_transform(feature_train.to_dict(orient='record'))
# #打印各个变量
#
#
#
# # 决策树， 训练
# # Train_data_inputs = Train_data[['BSSIDLabel', 'RSSLabel', 'SSIDLabel', 'finLabel']].values

# feature_test = Test_data[['BSSIDLabel', 'RSSLabel', 'SSIDLabel', 'finLabel']]
# Test_data_inputs_f = pd.get_dummies(feature_test)
#
# Train_data_inputs, Test_data_inputs = Train_data_inputs_f.align(Test_data_inputs_f,
#                                                                     join='left',
#                                                                     axis=1)
#
# print('show featuren',feature_train)
# print('show vectorn',Train_data_inputs)
# print('show vector namen',vec.get_feature_names())


# Test_data_inputs = vec.fit_transform(feature_test.to_dict(orient='record'))

# Test_data_inputs = Test_data[['BSSIDLabel', 'RSSLabel', 'SSIDLabel', 'finLabel']].values

