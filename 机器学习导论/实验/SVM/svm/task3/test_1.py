import numpy as np
import scipy.io as scio
from sklearn import svm

data = scio.loadmat('task3_train.mat')
data_t = scio.loadmat('task3_test.mat')
X = data['X']
y = data['y'].flatten()
X_t = data_t['X']
shape = np.shape(X)
shape_t = np.shape(X_t)
print('训练集样本数:%d,特征维度:%d' % (shape[0], shape[1]))
print('测试样本数:%d,特征维度:%d' % (shape_t[0], shape_t[1]))
print('Training Linear SVM (Spam Classification)')

c = 0.2
clf = svm.SVC(c, kernel='linear')
clf.fit(X, y)
p = clf.predict(X)
print('Training Accuracy: {}'.format(np.mean(p == y) * 100))

result = clf.predict(X_t)
np.savetxt('result.txt', result, fmt='%d', delimiter='\n')
# c = 0.1
# sigma = 0.1
# clf = svm.SVC(c, kernel='rbf', gamma=np.power(sigma, -2))

