#!/usr/local/bin/python2.7
#python findFeatures.py -t dataset/training/

import argparse as ap
import cv2
import numpy as np
import os
import joblib
from scipy.cluster.vq import *

from sklearn import preprocessing
# from rootsift import RootSIFT
import math

# Get the path of the training set
# parser = ap.ArgumentParser()
# parser.add_argument("-t", "--trainingSet", help="Path to Training Set", required="True")
# args = vars(parser.parse_args())
# train_path = args["trainingSet"]
# Get the training classes names and store them in a list

train_path = "dataset/training/"
training_names = os.listdir(train_path)
# Get all the path to the images and save them in a list
# image_paths and the corresponding label in image_paths
image_paths = []
for training_name in training_names:
    image_path = os.path.join(train_path, training_name)
    image_paths += [image_path]
# image_paths = image_paths[:50]

# Create feature extraction and keypoint detector objects
# fea_det = cv2.FeatureDetector_create("SIFT")
# des_ext = cv2.DescriptorExtractor_create("SIFT")
fea_det = cv2.SIFT_create()

# List where all the descriptors are stored
des_list = []

for i, image_path in enumerate(image_paths):
    im = cv2.imread(image_path)
    im_size = im.shape

    # print str(im.shape)
    # if im_size[1] > im_size[0]:
    #     im = cv2.resize(im,(imagesize_0,imagesize_1))
    # else:
    #     im = cv2.resize(im,(imagesize_1,imagesize_0))
    # print str(im.shape)

    im = cv2.resize(im, (im_size[1]//4, im_size[0]//4))

    print ("Extract SIFT of %s image, %d of %d images" %(training_names[i], i+1, len(image_paths)))
    # kpts = fea_det.detect(im)
    # kpts, des = des_ext.compute(im, kpts)
    # des.shape = [n, 128], n is the number of key points
    kpts, des = fea_det.detectAndCompute(im, None)
    # rootsift
    #rs = RootSIFT()
    #des = rs.compute(kpts, des)
    des_list.append((image_path, des))
    # print str(des.shape)  
    
# Stack all the descriptors vertically in a numpy array
downsampling = 2
descriptors = des_list[0][1][::downsampling,:]
for image_path, descriptor in des_list[1:]:
    # print np.size(descriptor)
    # print image_path
    # print descriptor
    descriptors = np.vstack((descriptors, descriptor[::downsampling,:]))

# Stack all the descriptors vertically in a numpy array
# descriptors = des_list[0][1]
# for image_path, descriptor in des_list[1:]:
#     print np.size(descriptor)
#     print descriptor
#     # if np.size(descriptor) != 0:
#     descriptors = np.vstack((descriptors, descriptor))  
numWords = 1000
# Perform k-means clustering
print("Start k-means: %d words, %d key points" %(numWords, descriptors.shape[0]))
voc, variance = kmeans(descriptors, numWords, 1) 
print('voc', voc.shape)
print('variance', variance)

# Calculate the histogram of features
im_features = np.zeros((len(image_paths), numWords), "float32")
for i in range(len(image_paths)):
    print("image number:"+str(i))
    words, distance = vq(des_list[i][1], voc)
    # print('words', type(words))
    # print('distance', type(distance))
    # print(words.shape)
    # print(distance.shape)
    for w in words:
        im_features[i][w] += 1
np.savetxt('im_features.csv', im_features, delimiter=',')


np.savetxt('features_im.csv', im_features.T, delimiter=',')


# Perform Tf-Idf vectorization
nbr_occurences = np.sum( (im_features > 0) * 1, axis = 0)
print('occur', nbr_occurences.shape)
idf = np.array(np.log((1.0*len(image_paths)+1) / (1.0*nbr_occurences + 1)), 'float32')
print('idf', idf)
# Perform L2 normalization
im_features = im_features*idf
im_features = preprocessing.normalize(im_features, norm='l2')

joblib.dump((im_features, image_paths, idf, numWords, voc), "bag-of-words.pkl", compress=3)        