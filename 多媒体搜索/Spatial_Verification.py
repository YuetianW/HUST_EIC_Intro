#!/usr/local/bin/python2.7
# python search.py -i dataset/testing/all_souls_000000.jpg
import matplotlib
import matplotlib.pyplot as plt


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
image_path = 'dataset/training/all_souls_000006.jpg'

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
im = cv2.resize(im, (im_size[1] // 4, im_size[0] // 4))

# kpts = fea_det.detect(im)
# kpts, des = des_ext.compute(im, kpts)
kpts, des = fea_det.detectAndCompute(im, None)

# rootsift
# rs = RootSIFT()
# des = rs.compute(kpts, des)

des_list.append((image_path, des))

# Stack all the descriptors vertically in a numpy array
descriptors = des_list[0][1]

#
test_features = np.zeros((1, numWords), "float32")
words, distance = vq(descriptors, voc)
for w in words:
    test_features[0][w] += 1

# Perform Tf-Idf vectorization and L2 normalization
test_features_origin = test_features * idf
test_features_origin = preprocessing.normalize(test_features_origin, norm='l2')

score = np.dot(test_features_origin, im_features.T)
rank_ID = np.argsort(-score)

# Relevance feedback
best_id = rank_ID[0][[1, 2, 4, 7, 8]]
worst_id = rank_ID[0][[3, 6, 9]]
a = 0.1
# new_test_f = 0.9 *test_features + 0.1*im_features[i for i in [13, 11]]
new_test_f = (1 - a * (len(best_id) + len(worst_id))) * test_features
for good in best_id:
    new_test_f = new_test_f + a * im_features[good]
for bad in worst_id:
    new_test_f = new_test_f - a * im_features[bad]
new_test_f *= idf
score_feedback = np.dot(new_test_f, im_features.T)
rank_ID_feedback = np.argsort(-score_feedback)

# 特 征 点 匹 配 函 数
def matchKeypoints(kpsA, featuresA, kpsB, featuresB, ratio):
    # 建立 Flann 匹配器
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE , trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params , search_params)
    matches = flann.knnMatch(featuresA, featuresB, k=2)
    good = []
    for m,n in matches:
        # 当 最 近 距 离 跟 次 近 距 离 的 比 值 小 于 ratio 值时 ， 保 留 此 匹 配 对
        if m.distance < ratio*n.distance:
            good.append([m])
    return good

# 对 检 索 结 果 与 检 索 图 片 的 匹 配 的 特 征 点 数 目 进 行 统 计
count_good = {}

imageA = cv2.imread(image_path)
(kpsA, featuresA) = fea_det.detectAndCompute(imageA, None)

for i in range(50):
    imageB = cv2.imread(image_paths[rank_ID[0][i]])
    (kpsB, featuresB) = fea_det.detectAndCompute(imageB, None)
    # 匹 配 两 张 图 片 的 所 有 特 征 点 ， 返 回 匹 配 结 果
    good = matchKeypoints(kpsA, featuresA, kpsB, featuresB, ratio=0.75)
    # 对 匹 配 结 果 进 行 绘 图 展 示
    match_img = cv2.drawMatchesKnn(imageA, kpsA, imageB, kpsB, good, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    # plt.figure(figsize=(16, 16))
    if i in range(6):
        plt.imshow(match_img[:, :, ::-1])
        plt.axis('off')
        plt.show()
    count_good[rank_ID[0][i]] = len(good)
print('finished!')
new_rank_ID = [i[0] for i in sorted(count_good.items(),
                key=lambda kv:(kv[1], kv[0]), reverse=True)]

# Visualize the results
figure()
gray()
subplot(5, 4, 1)
title('No Spatial Verification')
imshow(im[:, :, ::-1])
axis('off')
for i, ID in enumerate(rank_ID[0][0:16]):
    img = Image.open(image_paths[ID])
    gray()
    subplot(5, 4, i+5)
    imshow(img)
    axis('off')

plt.figure()
plt.subplot(5, 4, 1)
plt.title('Spatial Verification')
plt.imshow(imageA[:, :, ::-1])
plt.axis('off')

for i, ID in enumerate(new_rank_ID[0:16]):
    print(str(image_paths[ID]))
    img = Image.open(image_paths[ID])
    plt.subplot(5, 4, i+5)
    plt.imshow(img)
    plt.axis('off')
plt.show()