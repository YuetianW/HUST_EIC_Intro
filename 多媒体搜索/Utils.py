from sklearn.cluster import KMeans, MiniBatchKMeans
from Node import Node
opts = None
branches = None
maxDepth = None
model = None
Root = None

def InitModel():
	global model
	return

def BuildTree(Parent, Features, Depth):
	node = Node(Parent, Features.mean(axis=0), Depth)
	if Depth < maxDepth and Features.shape[0] >= 4*branches:
		model =  MiniBatchKMeans(n_clusters=branches)	# The KMeans Clustering Model
		model.fit(Features)
		for i in range(branches):
			node.pushChild(BuildTree(node, Features[model.labels_==i], Depth+1))
	else:
		Parent.setLeaf()
	return node

def LeafWeight(Leaf):
	pass

def FindFeatLeaf(Feat, Node):
	if Node.isLeaf:
		return Node
	else:
		index = np.argsort([np.linalg.norm(x.Feat-Feat) for x in Node.children])
		return FindFeatLeaf(Feat, Node.children[index])
