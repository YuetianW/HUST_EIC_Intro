# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 21:07:57 2018

@author: ASUS
"""
from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt

import time


def loadData(filename):
    """
    输入:
        数据集路径
    输出:
        numpy.array格式的X, y数据array
        X为m×n的数据array, m为样例数, n为特征维度
        y为m×1的标签array, 1表示正例, 0表示反例
    """

    dataDict = loadmat(filename)

    return dataDict['X'], dataDict['y']


def plotData(X, y, title=None):
    """
    作出原始数据的散点图
    X, y为loadData()函数返回的结果
    """

    X_pos = []
    X_neg = []

    sampleArray = np.concatenate((X, y), axis=1)
    for array in list(sampleArray):
        if array[-1]:
            X_pos.append(array)
        else:
            X_neg.append(array)

    X_pos = np.array(X_pos)
    X_neg = np.array(X_neg)

    fig = plt.figure()

    ax = fig.add_subplot(111)

    if title: ax.set_title(title)

    pos = plt.scatter(X_pos[:, 0], X_pos[:, 1], marker='+', c='b')
    neg = plt.scatter(X_neg[:, 0], X_neg[:, 1], marker='o', c='y')

    plt.legend((pos, neg), ('postive', 'negtive'), loc=2)

    plt.show()


def svmTrain_SMO(X, y, C, kernelFunction='linear', tol=1e-3, max_iter=5, **kargs):
    """
    利用简化版的SMO算法训练SVM
    （参考《机器学习实战》）
    
    输入：
    X, y为loadData函数的返回值
    C为惩罚系数
    kernelFunction表示核函数类型, 对于非线性核函数，也可直接输入核函数矩阵K
    tol为容错率
    max_iter为最大迭代次数
    
    输出：
    model['kernelFunction']为核函数类型
    model['X']为支持向量
    model['y']为对应的标签
    model['alpha']为对应的拉格朗日参数
    model['w'], model['b']为模型参数
    """

    start = time.perf_counter()

    m, n = X.shape
    X = np.mat(X)
    y = np.mat(y, dtype='float64')

    y[np.where(y == 0)] = -1

    alphas = np.mat(np.zeros((m, 1)))
    b = 0.0
    E = np.mat(np.zeros((m, 1)))
    iters = 0
    eta = 0.0
    L = 0.0
    H = 0.0

    if kernelFunction == 'linear':
        K = X * X.T
    elif kernelFunction == 'gaussian':
        K = kargs['K_matrix']
    else:
        print('Kernel Error')
        return None

    print('Training ...', end='')
    dots = 12
    while iters < max_iter:

        num_changed_alphas = 0
        for i in range(m):
            E[i] = b + np.sum(np.multiply(np.multiply(alphas, y), K[:, i])) - y[i]

            if (y[i] * E[i] < -tol and alphas[i] < C) or (y[i] * E[i] > tol and alphas[i] > 0):
                j = np.random.randint(m)
                while j == i:
                    j = np.random.randint(m)

                E[j] = b + np.sum(np.multiply(np.multiply(alphas, y), K[:, j])) - y[j]

                alpha_i_old = alphas[i].copy()
                alpha_j_old = alphas[j].copy()

                if y[i] == y[j]:
                    L = max(0, alphas[j] + alphas[i] - C)
                    H = min(C, alphas[j] + alphas[i])
                else:
                    L = max(0, alphas[j] - alphas[i])
                    H = min(C, C + alphas[j] - alphas[i])

                if L == H:
                    continue

                eta = 2 * K[i, j] - K[i, i] - K[j, j]
                if eta >= 0:
                    continue

                alphas[j] = alphas[j] - (y[j] * (E[i] - E[j])) / eta

                alphas[j] = min(H, alphas[j])
                alphas[j] = max(L, alphas[j])

                if abs(alphas[j] - alpha_j_old) < tol:
                    alphas[j] = alpha_j_old
                    continue

                alphas[i] = alphas[i] + y[i] * y[j] * (alpha_j_old - alphas[j])

                b1 = b - E[i] \
                     - y[i] * (alphas[i] - alpha_i_old) * K[i, j] \
                     - y[j] * (alphas[j] - alpha_j_old) * K[i, j]

                b2 = b - E[j] \
                     - y[i] * (alphas[i] - alpha_i_old) * K[i, j] \
                     - y[j] * (alphas[j] - alpha_j_old) * K[j, j]

                if (0 < alphas[i] and alphas[i] < C):
                    b = b1
                elif (0 < alphas[j] and alphas[j] < C):
                    b = b2
                else:
                    b = (b1 + b2) / 2.0

                num_changed_alphas = num_changed_alphas + 1

        if num_changed_alphas == 0:
            iters = iters + 1
        else:
            iters = 0

        print('.', end='')
        dots = dots + 1
        if dots > 78:
            dots = 0
            print()

    print('Done', end='')
    end = time.perf_counter()
    print('( ' + str(end - start) + 's )')
    print()

    idx = np.where(alphas > 0)
    model = {'X': X[idx[0], :], 'y': y[idx], 'kernelFunction': str(kernelFunction), \
             'b': b, 'alphas': alphas[idx], 'w': (np.multiply(alphas, y).T * X).T}
    return model


def visualizeBoundaryLinear(X, y, model, title=None):
    """
    X, y为loadData函数返回值
    model为svmTrain_SMO函数返回值
    """

    fig = plt.figure()
    ax = fig.add_subplot(111)

    w = model['w']
    b = model['b']
    xp = np.linspace(min(X[:, 0]), max(X[:, 0]), 100)
    yp = np.squeeze(np.array(- (w[0] * xp + b) / w[1]))

    ax.plot(xp, yp)

    # scatter
    X_pos = []
    X_neg = []

    sampleArray = np.concatenate((X, y), axis=1)
    for array in list(sampleArray):
        if array[-1]:
            X_pos.append(array)
        else:
            X_neg.append(array)

    X_pos = np.array(X_pos)
    X_neg = np.array(X_neg)

    if title: ax.set_title(title)

    pos = plt.scatter(X_pos[:, 0], X_pos[:, 1], marker='+', c='b')
    neg = plt.scatter(X_neg[:, 0], X_neg[:, 1], marker='o', c='y')

    plt.legend((pos, neg), ('postive', 'negtive'), loc=2)

    plt.show()


def gaussianKernelSub(x1, x2, sigma):
    """
    高斯核函数
    
    输入：
    x1, x2为向量
    sigma为高斯核参数
    """

    x1 = np.mat(x1).reshape(-1, 1)
    x2 = np.mat(x2).reshape(-1, 1)

    n = -(x1 - x2).T * (x1 - x2) / (2 * sigma ** 2)
    return np.exp(n)


def gaussianKernel(X, sigma):
    """
    计算高斯核函数矩阵
    """

    start = time.perf_counter()

    print('GaussianKernel Computing ...', end='')
    m = X.shape[0]
    X = np.mat(X)
    K = np.mat(np.zeros((m, m)))
    dots = 280
    for i in range(m):
        if dots % 10 == 0: print('.', end='')
        dots = dots + 1
        if dots > 780:
            dots = 0
            print()
        for j in range(m):
            K[i, j] = gaussianKernelSub(X[i, :].T, X[j, :].T, sigma)
            K[j, i] = K[i, j].copy()

    print('Done', end='')
    end = time.perf_counter()
    print('( ' + str(end - start) + 's )')
    print()
    return K


def svmPredict(model, X, *arg):
    """
    利用得到的model, 计算给定X的模型预测值
    
    输入：
    model为svmTrain_SMO返回值
    X为待预测数据
    sigma为训练参数
    """

    m = X.shape[0]
    p = np.mat(np.zeros((m, 1)))
    pred = np.mat(np.zeros((m, 1)))

    if model['kernelFunction'] == 'linear':
        p = X * model['w'] + model['b']
    else:
        for i in range(m):
            prediction = 0
            for j in range(model['X'].shape[0]):
                prediction += model['alphas'][:, j] * model['y'][:, j] * \
                              gaussianKernelSub(X[i, :].T, model['X'][j, :].T, *arg)

            p[i] = prediction + model['b']

    pred[np.where(p >= 0)] = 1
    pred[np.where(p < 0)] = 0

    return pred


def visualizeBoundaryGaussian(X, y, model, sigma):
    """
    分类边界可视化
    
    输入：
    X, y为loadData函数返回值
    model为svmTrain_SMO函数返回值
    """

    fig = plt.figure()
    ax = fig.add_subplot(111)

    x1plot = np.linspace(min(X[:, 0]), max(X[:, 0]), 100)
    x2plot = np.linspace(min(X[:, 1]), max(X[:, 1]), 100)
    X1, X2 = np.meshgrid(x1plot, x2plot)
    X1 = np.mat(X1)
    X2 = np.mat(X2)
    vals = np.mat(np.zeros(X1.shape))

    print('Predicting ...', end='')
    dots = 14
    for i in range(X1.shape[1]):
        print('.', end='')
        dots += 1
        if dots == 78:
            dots = 0
            print()
        this_X = np.concatenate((X1[:, i], X2[:, i]), axis=1)
        vals[:, i] = svmPredict(model, this_X, sigma)
    print('Done')

    ax.contour(X1, X2, vals, colors='black')
    # scatter
    X_pos = []
    X_neg = []

    sampleArray = np.concatenate((X, y), axis=1)
    for array in list(sampleArray):
        if array[-1]:
            X_pos.append(array)
        else:
            X_neg.append(array)

    X_pos = np.array(X_pos)
    X_neg = np.array(X_neg)

    pos = plt.scatter(X_pos[:, 0], X_pos[:, 1], marker='+', c='b')
    neg = plt.scatter(X_neg[:, 0], X_neg[:, 1], marker='o', c='y')

    plt.legend((pos, neg), ('postive', 'negtive'), loc=2)

    plt.show()
