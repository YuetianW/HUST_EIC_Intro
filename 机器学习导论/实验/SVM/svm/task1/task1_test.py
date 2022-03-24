import numpy as np
from matplotlib import pyplot as plt

import SVM_Functions as svmF

# X,y = svmF.loadData('task1_linear.mat')
# svmF.plotData(X,y)
# model = svmF.svmTrain_SMO(X, y, C=1, max_iter=20)
# svmF.visualizeBoundaryLinear(X, y, model)

X, y = svmF.loadData('task1_linear.mat')
svmF.plotData(X, y)


model = svmF.svmTrain_SMO(X, y, C=1, kernelFunction='gaussian', K_matrix=svmF.gaussianKernel(X, sigma=0.1))
svmF.visualizeBoundaryGaussian(X, y, model,sigma=0.1)
def visualize_boundary(clf, X, x_min, x_max, y_min, y_max):
    h = 0.02
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    plt.contour(xx, yy, Z, colors='r')


from sklearn import svm

clf = svm.SVC(C=1, kernel='linear', tol=1e-3)
clf.fit(X, y)
visualize_boundary(clf, X, 0, 4.5, 1.5, 5)
