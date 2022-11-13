import cv2
import numpy as np
from scipy.cluster.vq import *
from sklearn.preprocessing import normalize


import argparse
def myopts():
	parser = argparse.ArgumentParser()
	parser.add_argument('-database', default='inputs/database/', help='Path to database (default inputs/database)')
	parser.add_argument('-query', default='inputs/query/', help='Path to query (default inputs/query)')
	return parser.parse_args()

opts = myopts()
BASE_DATABASE_PATH = opts.database
BASE_QUERY_PATH = opts.query
NUM_CENTERS = 1000

DescList = []
DescImgMap = []
ImgList = []
sift = cv2.xfeatures2d.SIFT_create(1000)

print("Extracting SIFT Features...")


for i in range(54):
	for j in range(4):
		Path = BASE_DATABASE_PATH + str(i) + '_' + str(j+1) + '.png'
		img = cv2.imread(Path)
		if img is None:
			continue
		gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		_,des = sift.detectAndCompute(gray,None)
		DescList.append(des)
		DescImgMap.append(i)
		ImgList.append(Path)
if len(DescList)==0:
	print("Path Seems To Be Wrong : Recieved => " + BASE_DATABASE_PATH )		

print("SIFT Feature Extraction Completed...")
print("K Means Starting...")

CENTERS, _ = kmeans(np.vstack(DescList), NUM_CENTERS, 1) 

print("K Means Completed")
IMG_FEATS = np.zeros((len(DescList), NUM_CENTERS), "float32")
for i in range(len(DescList)):
	CLOSEST, _ = vq(DescList[i], CENTERS)
	np.add.at(IMG_FEATS[i], CLOSEST, 1)


IMG_FEATS = normalize(IMG_FEATS)

correct = 0
count = 0
for i in range(54):
	Path = BASE_QUERY_PATH + str(i) + '.png'
	img = cv2.imread(Path)
	if img is None:
		continue
	gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	_,des = sift.detectAndCompute(gray,None)
	TEST_FEATS = np.zeros(NUM_CENTERS)	
	CLOSEST, _ = vq(des, CENTERS)
	np.add.at(TEST_FEATS, CLOSEST, 1)
	TEST_FEATS = normalize(TEST_FEATS.reshape(1,-1))[0]
	TOP_FIVE = [DescImgMap[x] for x in np.argsort(np.dot(TEST_FEATS,IMG_FEATS.T)).tolist()[::-1][:5]]
	
	print("Image %d : "%(i), TOP_FIVE, "Correct" if i in TOP_FIVE else "InCorrect")
	correct = correct+1 if i in TOP_FIVE else correct
	count = count+1
print("Final Accuracy : %d/%d = %f"%(correct,count,correct/count))