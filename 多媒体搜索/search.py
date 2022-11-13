#!/usr/local/bin/python2.7
#python search.py -i dataset/testing/all_souls_000000.jpg
import matplotlib
# matplotlib.use('TkAgg')
import argparse as ap
import cv2
import imutils 
import numpy as np
import os
import joblib
from scipy.cluster.vq import *

from sklearn import preprocessing
import numpy as np

from pylab import *
from PIL import Image
# from rootsift import RootSIFT

# # Get the path of the training set
# parser = ap.ArgumentParser()
# parser.add_argument("-i", "--image", help="Path to query image", required="True")
# args = vars(parser.parse_args())
# # Get query image path
# image_path = args["image"]
image_path ='dataset/training/all_souls_000006.jpg'
feed_back = 0

# Load the classifier, class names, scaler, number of clusters and vocabulary 
im_features, image_paths, idf, numWords, voc = joblib.load("./bag-of-words.pkl")
    
# Create feature extraction and keypoint detector objects
# fea_det = cv2.FeatureDetector_create("SIFT")
# des_ext = cv2.DescriptorExtractor_create("SIFT")
fea_det = cv2.SIFT_create()

# List where all the descriptors are stored
des_list = []

im = cv2.imread(image_path)
im_size = im.shape
# print str(im.shape)
im = cv2.resize(im, (im_size[1]//4, im_size[0]//4))


# kpts = fea_det.detect(im)
# kpts, des = des_ext.compute(im, kpts)
kpts, des = fea_det.detectAndCompute(im, None)

# rootsift
#rs = RootSIFT()
#des = rs.compute(kpts, des)

des_list.append((image_path, des))   
    
# Stack all the descriptors vertically in a numpy array
descriptors = des_list[0][1]

# 
test_features = np.zeros((1, numWords), "float32")
words, distance = vq(descriptors, voc)
for w in words:
    test_features[0][w] += 1

# Perform Tf-Idf vectorization and L2 normalization
test_features_origin = test_features*idf
test_features_origin = preprocessing.normalize(test_features_origin, norm='l2')

score = np.dot(test_features_origin, im_features.T)
rank_ID = np.argsort(-score)

#Relevance feedback
best_id = rank_ID[0][[7, 10]]
worst_id = rank_ID[0][[5, 6]]
a = 0.2
# new_test_f = 0.9 *test_features + 0.1*im_features[i for i in [13, 11]]
new_test_f = (1-a * (len(best_id) + len(worst_id))) * test_features
for good in best_id:
	new_test_f = new_test_f + a * im_features[good]
for bad in worst_id:
	new_test_f = new_test_f - a * im_features[bad]
new_test_f *= idf
score_feedback = np.dot(new_test_f, im_features.T)
rank_ID_feedback = np.argsort(-score_feedback)


# Visualize the results
figure(1)
gray()
subplot(5, 4, 1)
title('No Relevance feedback')
imshow(im[:, :, ::-1])
axis('off')
for i, ID in enumerate(rank_ID[0][0:16]):
	img = Image.open(image_paths[ID])
	gray()
	subplot(5, 4, i+5)
	imshow(img)
	axis('off')
figure(2)
gray()
subplot(5, 4, 1)
title('Relevance feedback')
imshow(im[:, :, ::-1])
axis('off')
for i, ID in enumerate(rank_ID_feedback[0][0:16]):
	img = Image.open(image_paths[ID])
	gray()
	subplot(5, 4, i+5)
	imshow(img)
	axis('off')
show()
