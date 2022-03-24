import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn import metrics
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.manifold import MDS

# 预处理
def loaddata(filename):
    data_f = pd.read_csv(filename, encoding='gbk')
    imputer = SimpleImputer(missing_values=np.nan, strategy='constant', fill_value=-100)
    data = pd.DataFrame(imputer.fit_transform(data_f))
    data.columns = data_f.columns
    data_feature = data[['finLabel', 'BSSIDLabel', 'RSSLabel']]
    BSSID_v = list(set(data_f['BSSIDLabel']))
    BSSID_l = len(BSSID_v)
    data_bssid = data_feature.groupby('finLabel')
    data_input = []
    for i, v in data_bssid:  # 每个v仍为df
        tmp = np.array(v['BSSIDLabel'])
        rssdict = dict(zip(v['BSSIDLabel'], v['RSSLabel']))
        tmpa = BSSID_l * [0]
        for bssidv in BSSID_v:
            if bssidv in tmp:
                tmpa[BSSID_v.index(bssidv)] = rssdict[bssidv]
        data_input.append(tmpa)
    return data_input


X1 = loaddata('DataSetKMeans1.csv')
X2 = loaddata('DataSetKMeans2.csv')

Ks = range(2,8)
dbis = []
for i in Ks:
    kmeans_model = KMeans(n_clusters=i, random_state=1).fit(X1)
    labels = kmeans_model.labels_
    dbi = davies_bouldin_score(X1, labels)
    dbis.append(dbi)

plt.title('Relationship between DBI and K')
plt.xlabel('K')
plt.ylabel('DBI')
plt.plot(Ks,dbis)
plt.show()

# 可视化
# 将原始数据中的索引设置成聚类得到的数据类别
kmeans_model = KMeans(n_clusters=3, random_state=1).fit(X2)
labels = kmeans_model.labels_
mds = MDS(n_components=2, metric=True)
new_X_mds = mds.fit_transform(X1)
plt.scatter(new_X_mds [:,0], new_X_mds [:,1], c=labels)
plt.show()



