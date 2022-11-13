# Image-Retrieval
Image Retrieval using methods like Vocabulary-Tree & Bag-Of-Words

Image retrieval refers 	to task of retrieving the most similiar image from dataset and is a very important problem in Computer-Vision. Due to massive size of dataset we have removed dataset from the repository but rest of code works.

## Requirements
```
scipy
python-opencv
```

## Bag Of Words (BOW)
The Code is implemented in the file BOW.py
* First features are extracted from the images
* Then for these features K Means clustering is performed with 1000 clusters.
* Features are aligned to closest cluster centers
* Histograms are created for every image mapping them to cluster centers corresponding to their images
* While querying we build a corresponding histogram for the test image and find the most similiar histogram from the training images (via a simple dot product)

## Vocublary Tree
The Code is implemented in the file VocTree.py
* First the features are extracted from images
* The a tree is built recursively. The tree is represented via a `Node` object implemented in functions/Node.py. The buildTree function is implemented in functions/Utils.py
* Then images and leafs are then matched to each other building hash-maps from both sides.
* For every image, we use leaves as codebooks/histogram and determine how much each leaf weighs in for an image. This is implememented in lines 51-64 of VocTree.py
* While querying we build a corresponding leaf based histogram for the test image and find the most similiar histogram from the training images (via a simple dot product)