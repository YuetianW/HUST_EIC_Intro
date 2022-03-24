import numpy as np
import pandas as pd
from numpy import *
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


def load_BankNodeData():
    '''
    加载钞票数据集的训练集
    :return: 训练集的特征，训练集的label
    '''
    df = pd.read_csv(r'钞票训练集.txt', header=None)
    # trainSet = np.array(df.loc[:][[0, 1, 2, 3]].values)
    trainSet = np.array(df.loc[:][[0, 1, 2, 3]]) # trainSet.dtype = float64
    print('train set: \n', trainSet)
    labels = df.loc[:][4].values # labels.dtype = int64
    labels = np.where(labels == 1, 1, -1)
    print('lebel values: \n', labels)
    return trainSet, labels

def logisticRegression_SGD(trainSet, labels, eta = 0.01, max_iter = 5000):
    '''
    :param trainSet: 训练集
    :param labels: 训练集的y值
    :param eta: 学习率，步长
    :param iterTime: 最大迭代次数
    :return: 权重；权重更新记录，用户观测是否收敛
    '''
    sampleSize = len(labels)
    featureSize = len(trainSet[0]) + 1
    weights = random.rand(featureSize) # 权重
    weightsRecord = [[x] for x in weights] # 权重更新记录
    print('initial weights: ', weights)
    count = 0
    while(count < max_iter):
        sample = random.randint(0, sampleSize - 1)
        update = logisticFunction(-labels[sample] * (np.dot(weights[1:], trainSet[sample]) + weights[0]))
        weights[1:] = weights[1:] - eta * update * (-labels[sample] * trainSet[sample])
        weights[0] = weights[0] - eta * update * (-labels[sample])
        count += 1
        if count % 500 == 0:
            for i in range(featureSize):
                weightsRecord[i].append(weights[i])
    fout = open(r'weightRecord.txt', 'w', encoding='utf-8')
    for i in range(featureSize):
        fout.write(','.join([str(i) for i in weightsRecord[i]]) + '\n')
    fout.close()
    return weights, weightsRecord

def logisticFunction(inputV):
    '''
    logistic函数
    :param inputV: logistic函数输入
    :return: logistic函数值
    '''
    return 1.0 / (1.0 + np.exp(-inputV))


def plotWeightTrend():
    '''
    :return:
    '''
    df = pd.read_csv(r'weightRecord.txt', header=None)
    featureSize = df.values.shape[0]
    iter_n = df.values.shape[1]
    for i in range(featureSize):
        plt.plot(range(iter_n), df.loc[i], lw = 1.5, label = 'w_' + str(i))
    plt.legend(loc = 'upper left')
    plt.show()

def preformence_BankNodeData(weights):
    '''
    :param weights: 模型的权重
    :return: None
    '''
    df = pd.read_csv(r'钞票训练集.txt', header=None)
    testSet = df.loc[:][[0, 1, 2, 3]].values # shape = 26, 4, dtype = float64
    label = df.loc[:][4].values
    pre = np.dot(testSet, weights[1:]) + weights[0] # pre.shape = (26, ), dtype = float64
    error = 0
    for i in range(pre.__len__()):
        print('true labels\t:',label[i], 'predict\t:', np.where(logisticFunction(pre[i]) > 0.5, 1, 0), '(', logisticFunction(pre[i]), ')')
        error += np.where((np.where(logisticFunction(pre[i]) > 0.5, 1, 0)) != label[i], 1, 0)
    print('\033[1;32;40m error is', error / len(label), '\033[0m')


if __name__ == '__main__':
    trainSet, labels = load_BankNodeData()
    weights, weights_record = logisticRegression_SGD(trainSet, labels, 0.1, 1500000)
    plotWeightTrend()
    preformence_BankNodeData(weights)