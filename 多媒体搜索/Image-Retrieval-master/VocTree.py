import cv2
import numpy as np
from scipy.cluster.vq import *
from sklearn.preprocessing import normalize
from functions.Opts import myopts
import functions.Utils as U

opts = myopts()

#####################
BASE_DATABASE_PATH = opts.database
BASE_QUERY_PATH = opts.query

U.branches = opts.branches
U.maxDepth = opts.maxDepth
U.InitModel()
#####################

DescList = []
DescImgMap = []
ImgList = []
LeafImgList = []
sift = cv2.xfeatures2d.SIFT_create(1000)

DATA_SIZE = 54

print("Extracting SIFT Features...")


for i in range(DATA_SIZE):
	for j in range(4):
		Path = BASE_DATABASE_PATH + str(i) + '_' + str(j+1) + '.png'
		img = cv2.imread(Path)
		if img is None:
			continue
		gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		_,des = sift.detectAndCompute(gray,None)
		DescList.append(des)
		DescImgMap.append((i,j))
		ImgList.append(Path)
		LeafImgList.append({})
if len(DescList)==0:
	print("Path Seems To Be Wrong : Recieved => " + BASE_DATABASE_PATH )		
print("SIFT Feature Extraction Completed...")

print("Building The Tree...")

Root = U.BuildTree(-1, np.vstack(DescList), 0)
U.Root = Root

for i,desc in enumerate(DescList):
	for des in desc:
		Root.tfidf(des, DescImgMap[i])

Leaves = Root.allLeaves()

for leaf in Leaves:
	for i,mapp in enumerate(DescImgMap):
		if mapp in leaf.Images:
			LeafImgList[i][leaf] = (leaf.Images[mapp]*leaf.weight())
		else:
			LeafImgList[i][leaf] = 0

LeafImgList = [{y : z/sum(list(x.values())) for y,z in x.items()} for x in LeafImgList]


print("Built The Tree...")

print("Testing...")


correct = 0
count = 0
for i in range(DATA_SIZE):
	Path = BASE_QUERY_PATH + str(i) + '.png'
	img = cv2.imread(Path)
	if img is None:
		continue
	gray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	_,des = sift.detectAndCompute(gray,None)
	q = {leaf:0 for leaf in Leaves}

	for d in des:
		leaf = Root.query(d)
		q[leaf] = q[leaf] + 1 if leaf in q else 1

	q = {y : y.weight()*z/sum(q.values()) for y,z in q.items()}	
	

	TOP_FIVE = [(-1e8,None) for i in range(5)]
	for j,lidict in enumerate(LeafImgList):
		score = 0
		for leaf in Leaves:
			if leaf in lidict and leaf in q:
				score += q[leaf]*lidict[leaf]#abs(q[leaf] - lidict[leaf])

		TOP_FIVE.append((score,DescImgMap[j][0]))
		TOP_FIVE = sorted(TOP_FIVE, key=lambda x: x[0])[::-1][:5]

	TOP_FIVE = [x[1] for x in TOP_FIVE]
	print("Image %d : "%(i), TOP_FIVE, "Correct" if i in TOP_FIVE else "InCorrect")
	correct = correct+1 if i in TOP_FIVE else correct
	count = count+1

print("Final Accuracy : %d/%d = %f"%(correct,count,correct/count))