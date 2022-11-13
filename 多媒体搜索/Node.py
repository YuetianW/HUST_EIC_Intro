import numpy as np
import math

flatten = lambda x : [z for y in x for z in y]
class Node(object):
	"""docstring for Node"""
	def __init__(self, Parent, Feat, Depth):
		super(Node, self).__init__()
		self.Parent = Parent
		self.Feat = Feat
		self.Depth = Depth
		self.children = []
		self.isLeaf = False

	def pushChild(self, child):
		self.children.append(child)
	
	def setLeaf(self):
		self.isLeaf = True
		setattr(self, "Images", {})

	def tfidf(self, des, i):
		if self.isLeaf:
			self.Images[i] = self.Images[i]+1 if i in self.Images else 1
		else:
			#print('Push Images Not a Leaf ')
			index = np.argsort([np.linalg.norm(x.Feat-des) for x in self.children])[0]
			self.children[index].tfidf(des, i)

	def allLeaves(self):
		if self.isLeaf:
			return [self]
		else:
			return flatten([x.allLeaves() for x in self.children])

	def weight(self):
		if self.isLeaf:
			return math.log1p(500/1.0*len(self.Images))
		else:
			print('weight : not a leaf')
			return None

	def query(self, des):
		if self.isLeaf:
			return self
		else:
			#print('Push Images Not a Leaf ')
			index = np.argsort([np.linalg.norm(x.Feat-des) for x in self.children])[0]
			return self.children[index].query(des)