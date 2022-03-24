from matplotlib import pyplot as plt
import Kmeansch10 as km

data_X = km.loadDataSet("places.txt")
centroids, clusterAssment = km.kMeans(data_X, 4)

plt.figure()
plt.scatter(data_X[:, 0].flatten().tolist(), data_X[:, 1].flatten().tolist(), c="b", marker="o")
plt.scatter(centroids[:, 0].flatten().tolist(), centroids[:, 1].flatten().tolist(), c='r', marker="+")
plt.show()
