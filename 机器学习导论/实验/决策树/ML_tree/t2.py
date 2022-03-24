import numpy as np
import scipy as sp
from sklearn import tree
from sklearn.cross_validation import train_test_split
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import classification_report

def main():
    data = []
    lable= []
    with open("decisiontree.txt") as ifile:
        for line in ifile:
            tmp = line.strip().split(' ')
            tmp1=[]
            for i in range(0,len(tmp)-1):
                tmp1.append(float(tmp[i]))
            data.append(tmp1)
            lable.append(float(tmp[len(tmp)-1]))

    x = np.array(data)
    y = np.array(lable)

    ''''' 拆分训练数据与测试数据 '''
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2)

    ''''' 使用信息熵作为划分标准，对决策树进行训练 '''
    clf = tree.DecisionTreeClassifier(criterion='entropy')
    print(clf)
    clf.fit(x_train, y_train)

    ''''' 把决策树结构写入文件 '''
    with open("tree.dot", 'w') as f:
        f = tree.export_graphviz(clf, out_file=f)

    ''''' 系数反映每个特征的影响力。越大表示该特征在分类中起到的作用越大 '''
    print(clf.feature_importances_)

    '''''测试结果的打印'''
    answer = clf.predict(x_train)
    print(x_train)
    print(answer)
    print(y_train)
    print(np.mean( answer == y_train))

    '''''准确率与召回率'''
    precision, recall, thresholds = precision_recall_curve(y_train, clf.predict(x_train))
    answer = clf.predict_proba(x)[:,1]
    print(classification_report(y, answer, target_names = ['yes', 'no']))


if __name__ == '__main__':
    main()