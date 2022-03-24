import pandas as pd

import SVM_Functions as svmF

X, y = svmF.loadData('task2.mat')
svmF.plotData(X, y)

model = svmF.svmTrain_SMO(X, y, C=1, kernelFunction='gaussian', K_matrix=svmF.gaussianKernel(X, sigma=0.1))
svmF.visualizeBoundaryGaussian(X, y, model,sigma=0.1)


# Clist = [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30]
# slist = [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30]
# dlist = pd.DataFrame(columns=Clist, index=slist)
# dlist.index.name = 'sigma'
# dlist.columns.name = 'C'