# import matplotlib.pyplot as plt
# import numpy as np
# import scipy.io as scio
# from sklearn import svm
#
# plt.ion()
# np.set_printoptions(formatter={'float': '{: 0.6f}'.format})
#
# data = scio.loadmat('task1_linear.mat')
# X = data['X']
# y = data['y'].flatten()
# m = y.size
#
#
# def plot_data(X, y):
#     plt.figure()
#
#     pos = np.where(y == 1)[0]
#     neg = np.where(y == 0)[0]
#
#     plt.scatter(X[pos, 0], X[pos, 1], marker="+", c='b')
#     plt.scatter(X[neg, 0], X[neg, 1], marker="o", c='y', s=15)
#
#
# def visualize_boundary(clf, X, x_min, x_max, y_min, y_max):
#     h = 0.02
#     xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
#
#     Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
#     Z = Z.reshape(xx.shape)
#     plt.contour(xx, yy, Z, levels=[0], colors='r')
#
# from sklearn import svm
# c = 1
# clf = svm.SVC(c, kernel='linear', tol=1e-3)
# clf.fit(X, y)
#
# plot_data(X, y)
# visualize_boundary(clf, X, 0, 4.5, 1.5, 5)
#
# data = scio.loadmat('task1_gaussian.mat')
# X = data['X']
# y = data['y'].flatten()
# m = y.size
# plot_data(X, y)
# c = 1
# sigma = 0.1
# clf = svm.SVC(c, kernel='rbf', gamma=np.power(sigma, -2))
# clf.fit(X, y)
# plot_data(X, y)
# visualize_boundary(clf, X, 0, 1, .4, 1.0)
