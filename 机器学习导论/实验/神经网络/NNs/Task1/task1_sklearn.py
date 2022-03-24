# -*- coding:UTF-8 -*-
import numpy as np
from sklearn.linear_model import LogisticRegression

def colicSklearn():
    #使用np读取数据
    trainFiled=np.loadtxt('horseColicTraining.txt',delimiter="\t")
    trainSet = trainFiled[:,:-1]
    trainLables=trainFiled[:,-1:]

    testFiled = np.loadtxt('horseColicTest.txt', delimiter="\t")
    testSet = testFiled[:, :-1]
    testLables = testFiled[:, -1:]
    classifier=LogisticRegression(solver='liblinear',max_iter=10).fit(trainSet,trainLables)
    test_accurcy=classifier.score(testSet,testLables) *100

    print('正确率：%f%%'%test_accurcy)
if __name__ == '__main__':
    colicSklearn()
