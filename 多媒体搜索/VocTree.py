import cv2
import numpy as np
from scipy.cluster.vq import *
from sklearn.preprocessing import normalize
from Opts import myopts
import Utils as U
import os
import warnings
from matplotlib.pyplot import *
from PIL import Image
warnings.filterwarnings("ignore")
opts = myopts()
import matplotlib
#####################
BASE_DATABASE_PATH = 'dataset\\training'
BASE_QUERY_PATH = 'dataset\\testing'

U.branches = opts.branches
U.maxDepth = opts.maxDepth
U.InitModel()
#####################

DescList = []
DescImgMap = []
ImgList = []
LeafImgList = []
sift = cv2.SIFT_create(1000)

# DATA_SIZE = 54
training_names = os.listdir(BASE_DATABASE_PATH)

image_paths = []
for training_name in training_names:
	image_path = os.path.join(BASE_DATABASE_PATH, training_name)
	image_paths += [image_path]

DATA_SIZE = len(image_paths)
print(DATA_SIZE)
print("Extracting SIFT Features...")


for i in range(DATA_SIZE):
		#Path = BASE_DATABASE_PATH + str(i) + '_' + str(j+1) + '.jpg'
		img = cv2.imread(image_paths[i])
		if img is None:
			continue
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		_, des = sift.detectAndCompute(gray, None)
		DescList.append(des)
		DescImgMap.append(i)
		ImgList.append(image_paths[i])
		LeafImgList.append({})
if len(DescList)==0:
	print("Path Seems To Be Wrong : Recieved => " + BASE_DATABASE_PATH)
print("SIFT Feature Extraction Completed...")

print("Building The Tree...")
#print(DescList)
Root = U.BuildTree(-1, np.vstack(DescList), 0)
U.Root = Root

for i, desc in enumerate(DescList):
	for des in desc:
		Root.tfidf(des, DescImgMap[i])

Leaves = Root.allLeaves()

for leaf in Leaves:
	for i, mapp in enumerate(DescImgMap):
		if mapp in leaf.Images:
			LeafImgList[i][leaf] = (leaf.Images[mapp]*leaf.weight())
		else:
			LeafImgList[i][leaf] = 0

LeafImgList = [{y: z/sum(list(x.values())) for y, z in x.items()} for x in LeafImgList]


print("Tree Building Done!")

print("Testing...")


correct = 0
count = 0

testing_names = os.listdir(BASE_QUERY_PATH)

image_paths2 = []
for test_name in testing_names:
	image_path2 = os.path.join(BASE_QUERY_PATH, test_name)
	image_paths2 += [image_path2]

DATA_SIZE2 = len(image_paths2)

for i in range(DATA_SIZE2):
	#Path = BASE_QUERY_PATH + str(i) + '.png'
	img = cv2.imread(image_paths2[i])
	if img is None:
		continue
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	_, des = sift.detectAndCompute(gray, None)
	q = {leaf:0 for leaf in Leaves}

	for d in des:
		leaf = Root.query(d)
		q[leaf] = q[leaf] + 1 if leaf in q else 1

	q = {y: y.weight()*z/sum(q.values()) for y, z in q.items()}

	TOP_FIVE = [(-1e8, None) for k in range(5)]
	for j, lidict in enumerate(LeafImgList):
		score = 0
		for leaf in Leaves:
			if leaf in lidict and leaf in q:
				score += q[leaf]*lidict[leaf]#abs(q[leaf] - lidict[leaf])
				# print(score)

		TOP_FIVE.append((score, DescImgMap[j]))
		TOP_FIVE = sorted(TOP_FIVE, key=lambda x: x[0])[::-1][:5]

	TOP_FIVE = [training_names[x[1]] for x in TOP_FIVE]
	print(testing_names[i], TOP_FIVE, "Correct" if testing_names[i] in TOP_FIVE else "InCorrect")
	correct = correct+1 if testing_names[i] in TOP_FIVE else correct
	count = count+1
print(count)
print("Final Accuracy : %d/%d = %2f" % (correct, count, correct/count))

Path = 'dataset/training/all_souls_000006.jpg'
img = cv2.imread(Path)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, des = sift.detectAndCompute(gray, None)
q = {leaf: 0 for leaf in Leaves}

for d in des:
	leaf = Root.query(d)
	q[leaf] = q[leaf] + 1 if leaf in q else 1

q = {y: y.weight() * z / sum(q.values()) for y, z in q.items()}

top = []

for j, lidict in enumerate(LeafImgList):
	score = 0
	for leaf in Leaves:
		if leaf in lidict and leaf in q:
			score += q[leaf] * lidict[leaf] # abs(q[leaf] − lidict[leaf])
	top.append((score, j))
	top = sorted(top, key=lambda x: x[0])[::-1]


# Visualize the results
figure(1)
subplot(5, 4, 1)
title('Vocabulary Tree')
imshow(img[:, :, ::-1])
axis('off')
for i, item in enumerate(top[0:16]):
	img = Image.open(image_paths[item[1]])
	subplot(5, 4, i+5)
	imshow(img)
	axis('off')
savefig("1.jpg")
show()


# 空间校验


# 特 征 点 匹 配 函 数
def matchKeypoints(kpsA, featuresA, kpsB, featuresB, ratio):
    # 建立 Flann 匹配器
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE , trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(featuresA, featuresB, k=2)
    good = []
    for m,n in matches:
        # 当 最 近 距 离 跟 次 近 距 离 的 比 值 小 于 ratio 值时 ， 保 留 此 匹 配 对
        if m.distance < ratio*n.distance:
            good.append([m])
    return good

# 对 检 索 结 果 与 检 索 图 片 的 匹 配 的 特 征 点 数 目 进 行 统 计
count_good = {}
fea_det = cv2.SIFT_create()
imageA = cv2.imread(Path)
(kpsA, featuresA) = fea_det.detectAndCompute(imageA, None)


for i in range(128):
    imageB = cv2.imread(image_paths[top[i][1]])
    (kpsB, featuresB) = fea_det.detectAndCompute(imageB, None)
    # 匹 配 两 张 图 片 的 所 有 特 征 点 ， 返 回 匹 配 结 果
    good = matchKeypoints(kpsA, featuresA, kpsB, featuresB, ratio=0.75)
    # 对 匹 配 结 果 进 行 绘 图 展 示
    match_img = cv2.drawMatchesKnn(imageA, kpsA, imageB, kpsB, good, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    # plt.figure(figsize=(16, 16))
    count_good[top[i][1]] = len(good)
print('finished!')
new_rank_ID = [i[0] for i in sorted(count_good.items(),
                key=lambda kv:(kv[1], kv[0]), reverse=True)]

figure(figsize=(16, 16))
subplot(5, 4, 1)
imshow(imageA[:, :, ::-1])
axis('off')

for i, ID in enumerate(new_rank_ID[0:16]):
    print(str(image_paths[ID]))
    img = Image.open(image_paths[ID])
    subplot(5, 4, i+5)
    imshow(img)
    axis('off')
savefig("2.jpg")
show()