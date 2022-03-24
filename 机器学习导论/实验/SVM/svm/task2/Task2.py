import numpy as np
import pandas as pd
import scipy.io as sio
import scipy.optimize as opt
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn import svm
import math
import pandas as pd

''' Loading and Visualizing Data '''


def Get_Data(path):
    data = sio.loadmat(path)
    # for key in data:
    #     print(key)
    return data, data['X'], data['y']


def Plot_Data(data):
    data1 = data['X'][np.where(data['y'].ravel() == 1)]  # positive examples
    data2 = data['X'][np.where(data['y'].ravel() == 0)]
    plt.plot(data1[:, 0], data1[:, 1], 'k+')
    plt.plot(data2[:, 0], data2[:, 1], 'yo')
    plt.show()
    return plt


def Plot_Boundary(X, classifier):
    x1 = np.linspace(min(X[:, 0]), max(X[:, 0]), 500)  # 第一特征
    x2 = np.linspace(min(X[:, 1]), max(X[:, 1]), 500)
    x1, x2 = np.meshgrid(x1, x2)
    # print(x1.shape,x2.shape) # 100*100
    grid = np.stack((x1.flat, x2.flat), axis=1)
    # print(grid.shape) # 10000*2
    grid_predict = classifier.predict(grid)
    grid_predict = grid_predict.reshape(x1.shape)  # 还原成网格形状
    plt = Plot_Data(data)
    plt.xlim(-0.6, 0.3)
    plt.ylim(-0.8, 0.6)
    plt.contour(x1, x2, grid_predict)
    plt.title('SVM Decision Boundary with C = 1, sigma = 0.1 ', fontsize=12)
    plt.show()


''' Training Linear SVM(try C=1,100) '''


def Train_SVM(data, X, y, C, sigma):
    classifier = svm.SVC(C=C, kernel='rbf', gamma=math.pow(sigma, -2.0) / 2, decision_function_shape='ovr')
    classifier.fit(X, y.ravel())
    Plot_Boundary(X, classifier)


def GaussianKernel(x1, x2, sigma):  # 求向量x1与向量x2的相似度
    sim = math.exp(-((x1 - x2) ** 2).sum() / (2 * sigma * sigma))
    return sim


''' try differcent C and sigma in {0.01,0.03,0.1,0.3,1,3,10,30} '''


def Find_Best_Param(X, y, Xval, yval):
    C_best = 0
    sigma_best = 0
    Clist = [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30]
    slist = [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30]
    predict_best = 0.0
    dlist = pd.DataFrame(columns=Clist, index=slist)
    dlist.index.name = 'sigma'
    dlist.columns.name = 'C'
    for C_now in Clist:
        for sigma_now in slist:
            classifier = svm.SVC(C=C_now, kernel='rbf', gamma=np.power(sigma_now, -2.0) / 2, decision_function_shape='ovr')
            classifier.fit(X, y)
            predict = classifier.score(Xval, yval)  # Returns the mean accuracy on the given test data and labels
            dlist.loc[sigma_now, C_now] = predict
            if predict > predict_best:
                predict_best, C_best, sigma_best = predict, C_now, sigma_now
    print("Accuracy List:")
    print(dlist)
    return C_best, sigma_best, predict_best


def Test_function():
    ''' test gaussiankernel function '''
    x1 = np.array([1, 2, 1])
    x2 = np.array([0, 4, -1])
    sigma = 2
    sim = GaussianKernel(x1, x2, sigma)
    print(sim)  # expect to see 0.32465247


data, X, y = Get_Data('task2.mat')  # 路径可改
# Plot_Data(data)
C, sigma, prediction = Find_Best_Param(X, y.ravel(), data['Xval'], data['yval'].ravel())
print("最优参数为：")
print(C, sigma, prediction)  # expect to see: 1 0.1 0.965
Train_SVM(data, X, y, C, sigma)
