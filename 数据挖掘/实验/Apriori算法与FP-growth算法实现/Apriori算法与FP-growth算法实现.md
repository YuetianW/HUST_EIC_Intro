# Apriori 算法与FP-growth算法实现

[TOC]

## **一．**  **实验目的**

1．加强对Apriori 算法与FP-growth算法的理解;

2．锻炼分析问题、解决问题并动手实践的能力。

 

## **二．**  **实验任务**

用一种你熟悉的程序设计语，实现Apriori算法与FP-growth，在数据集上比较算法的性能。

 

## **三．**  **实验背景**

现在，数据挖掘作为从数据中获取信息的有效方法，越来越受到人们的重视。关联规则挖掘首先是用来发现购物篮数据事务中各项之间的有趣联系。从那以后，关联规则就成为数据挖掘的重要研究方向,它是要找出隐藏在数据间的相互关系。目前关联规则挖掘的研究工作主要包括:Apriori算法的扩展、数量关联规则挖掘、关联规则增量式更新、无须生成候选项目集的关联规则挖掘、最大频繁项目集挖掘、约束性关联规则挖掘以及并行及分布关联规则挖掘算法等。关联规则的挖掘问题就是在事务数据库D中找出具有用户给定的满足一定条件的最小支持度Minsup和最小置信度Minconf的关联规则。

从大规模的数据中发现物品间隐含关系的方法被称为关联分析。关联分析是一种在大规模数据集中寻找有趣关系的任务。

**关联规则:**

关联规则是形如X→Y的表达式，其中X和Y是不相交的项集，即X∩Y=∅。关联规则的强度可以用它的支持度（support）和置信度（confidence）来度量。支持度确定规则可以用于给定数据集的频繁程度，而置信度确定Y在包含X的交易中出现的频繁程度。

**支持度**（表示X和Y同时在总数N中发生的概率）:

​                               

 

**置信度**（在发生X的项集中，同时会发生Y的概率，即X和Y同时发生的样本数占仅仅X发生样本数的比例）:

 

 

**提升度**（在发生X的条件下，同时发生Y的概率，与只发生Y的概率之比。提升度反映了关联规则中的X与Y的相关性，提升度>1且越高表明正相关性越高，提升度<1且越低表明负相关性越高，提升度=1表明没有相关性，即相互独立）:

 

 

**频繁项集:**

项集是指若干个项的集合。频繁项集是指支持度大于等于最小支持度(min_sup)的集合。

 

 

## **四．**  **算法原理**

**1.**  **Apriori****算法：**



**a)**  **算法描述：**

Apriori算法是一种找频繁项目集的基本算法。其基本原理是逐层搜索的迭代:频繁K项Lk集用于搜索频繁(K+1)项集 Lk+1，如此下去，直到不能找到维度更高的频繁项集为止。这种方法依赖连接和剪枝这两步来实现。算法的第一次遍历仅仅计算每个项目的具体值的数量，以确定大型l项集。随后的遍历，第k次遍历，包括两个阶段。首先，使用在第(k-1)次遍历中找到的大项集Lk-1和产生候选项集Ck。接着扫描数据库，计算Ck中候选的支持度。用Hash树可以有效地确定Ck中包含在一个给定的事务t中的候选。如果某项集满足最小支持度，则称它为频繁项集。

 

**b)**  **算法流程：**

步骤如下:

①  设定最小支持度s和最小置信度c;

②  Apriori算法使用候选项集。首先产生出候选的项的集合,即候选项集,若候选项集的支持度大于或等于最小支持度,则该候选项集为频繁项集;

③  在 Apriori算法的过程中,首先从数据库读入所有的事务,每个项都被看作候选1-项集,得出各项的支持度,再使用频繁1-项集集合来产生候选2-项集集合,因为先验原理保证所有非频繁的1-项集的超集都是非频繁的;

④  再扫描数据库,得出候选2-项集集合,再找出频繁2-项集,并利用这些频繁2-项集集合来产生候选3-项集;

⑤  重复扫描数据库,与最小支持度比较,产生更高层次的频繁项集,再从该集合里产生下一级候选项集,直到不再产生新的候选项集为止。

 

 

\2.  FP-growth算法：

a)  需求分析：

数据挖掘是从数据库中提取隐含的、未知的和潜在的有用信息的过程,是数据库及相关领域研究中的一个极其重要而又具有广阔应用前景的新领域﹒目前,对数据挖掘的研究主要集中在分类、聚类、关联规则挖掘、序列模式发现、异常和趋势发现等方面,其中关联规则挖掘在商业等领域中的成功应用使它成为数据挖掘中最重要、最活跃和最成熟的研究方向.现有的大多数算法均是以Apriori 先验算法为基础的,产生关联规则时需要生成大量的候选项目集.为了避免生成候选项目集,Han等提出了基于FP树频繁增长模式(Frequent-PatternGrowth，FP-Growth）算法。

 

b)  算法流程：

FP树的构造过程可描述为:首先创建树的根结点，用“null”标记.扫描交易数据集DB ,每个事务中的项目按照支持度递减排序,并对每个事务创建一个分枝.一般地,当为一个事务考虑增加分枝时,沿共同前缀上的每个结点的计数值增加1为跟随在前缀之后的项目创建结点并链接.为方便树的遍历,创建一个频繁项目列表,使得每个项目通过一个结点头指针指向它在树中的位置.FP树挖掘过程可描述为:由长度为1的频繁项目开始,构造它的条件项目基和条件FP树,并递归地在该树上进行挖掘.项目增长通过后缀项目与条件FP树产生的频繁项目连接实现.FP-Growth算法将发现大频繁项目集的问题转换成递归地发现一些小频繁项目,然后连接后缀.它使用最不频繁的项目后缀,提供了好的选择性。

##  **五．**  **具体实现**

**1.**  **数据集：**

使用经典的超市购物篮数据集：http://fimi.uantwerpen.be/data/

Retail Market Basket Data Set

**描述如下：**

![在这里插入图片描述](https://img-blog.csdnimg.cn/392eff80673e4fbf830731166958d286.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzQ5OTI5Mg==,size_16,color_FFFFFF,t_70)


​                               

This document describes the retail market basket data set supplied by a anonymous Belgian retail supermarket store. The document describes the contents of the data, the period over which the data were collected, some characteristics of the data and legal issues with respect to the use of this data set.

 

**2.**  **Apriori****算法：**

**代码思路：**

频繁项集（Frequent Itemset）的生成：生成所有supoort>= minsup的项集合

关联规则的生成：对每一个频繁项集（XY）进行二元划分，生成confidence最高的一系列规则（X->Y）

Apriori 算法思想：（购买A、B、C频繁则分别购买AB、BC、AC、ABC肯定频繁）频繁项集的子集也是频繁项集

 

**代码实现：**

```python
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 14:44:20 2021

@author: Yuetian
"""

import pandas as pd
import numpy as np
from itertools import combinations
from operator import itemgetter
from time import time
import warnings
warnings.filterwarnings("ignore")
# 拿到购物栏数据

dataset = pd.read_csv('t1.csv', usecols=['items'])

# 定义自己的Aprior算法
def my_aprior(data, support_count):
    """
    Aprior关联规则挖掘
    @data: 数据
    @support_count: 项集的频度, 最小支持度计数阈值
    """
    start = time()
    # 对数据进行处理，删除多余空格
    for index, row in data.iterrows():
        data.loc[index, 'items'] = row['items'].strip()
    # 找出所有频繁一项集
    single_items = (data['items'].str.split(" ", expand = True)).apply(pd.value_counts) \
    .sum(axis = 1).where(lambda value: value > support_count).dropna()
    print("找到所有频繁一项集")
    # 创建频繁项集对照表
    apriori_data = pd.DataFrame({'items': single_items.index.astype(int), 'support_count': single_items.values, 'set_size': 1})
    # 整理数据集
    data['set_size'] = data['items'].str.count(" ") + 1
    data['items'] = data['items'].apply(lambda row: set(map(int, row.split(" "))))
    single_items_set = set(single_items.index.astype(int))
    # 循环计算，找到频繁项集
    for length in range(2, len(single_items_set) + 1):
        data = data[data['set_size'] >= length]
        d = data['items'] \
            .apply(lambda st: pd.Series(s if set(s).issubset(st) else None for s in combinations(single_items_set, length))) \
            .apply(lambda col: [col.dropna().unique()[0], col.count()] if col.count() >= support_count else None).dropna()
        if d.empty:
            break
        apriori_data = apriori_data.append(pd.DataFrame(
            {'items': list(map(itemgetter(0), d.values)), 'support_count': list(map(itemgetter(1), d.values)),
             'set_size': length}), ignore_index=True)
    print("结束搜索，总耗时%s"%(time() - start))
    return apriori_data

apriori_result = my_aprior(dataset, 5000)
for x in apriori_result:
    print(x)

```

**1.**  **FG-growth****：**

**代码思路：**

首先挖掘频率低的项，然后逐次挖掘频率高的项。

首先挖掘频率最低的项F，因为其子树恰好较为简单，所以可以很容易地得到其条件模式基。

条件模式基（conditional pattern base）：条件模式基是以所查找项为结尾的路径集合。每一条路径其实都是一条前缀路径。

简而言之，一条前缀路径是介于所查找元素项与树根节点之间的所有内容。对于一颗conditional FP-tree(条件FP树)，可以进行递归的挖掘(合并分支等)。

 

**代码实现：**

\

```python
# -*- coding: utf-8 -*-

"""

Created on Mon Apr 12 17:12:25 2021

 

@author: Yuetian

"""

import pandas as pd

import numpy as np

from itertools import combinations

from operator import itemgetter

from time import time

 

class treeNode:

  def __init__(self, nameValue, numOccur, parentNode):

​    self.name = nameValue # 存放结点名字

​    self.count = numOccur # 计数器

​    self.nodeLink = None # 连接相似结点

​    self.parent = parentNode # 存放父节点，用于回溯

​    self.children = {} # 存放子节点

 

  def inc(self, numOccur):

​    self.count += numOccur

 

  def disp(self, ind=1):

​    \# 输出调试用

​    print(' '*ind, self.name, ' ', self.count)

​    for child in self.children.values():

​      child.disp(ind+1)

 

def updateHeader(nodeToTest, targetNode):

  """

  设置头结点

  @nodeToTest: 测试结点

  @targetNode: 目标结点

  """

  while nodeToTest.nodeLink != None:

​    nodeToTest = nodeToTest.nodeLink

  nodeToTest.nodeLink = targetNode

 

def updateFPtree(items, inTree, headerTable, count):

  """

  更新FP-Tree

  @items: 读取的数据项集

  @inTree: 已经生成的树

  @headerTable: 链表的头索引表

  @count: 计数器

  """

  if items[0] in inTree.children:

​    \# 判断items的第一个结点是否已作为子结点

​    inTree.children[items[0]].inc(count)

  else:

​    \# 创建新的分支

​    inTree.children[items[0]] = treeNode(items[0], count, inTree)

​    if headerTable[items[0]][1] == None:

​      headerTable[items[0]][1] = inTree.children[items[0]]

​    else:

​      updateHeader(headerTable[items[0]][1], inTree.children[items[0]])

  \# 递归

  if len(items) > 1:

​    updateFPtree(items[1::], inTree.children[items[0]], headerTable, count)

 

def createFPtree(dataSet, minSup=1):

  """

  建立FP-Tree

  @dataset: 数据集

  @minSup: 最小支持度

  """

  headerTable = {}

  for trans in dataSet:

​    for item in trans:

​      headerTable[item] = headerTable.get(item, 0) + dataSet[trans]

  for k in list(headerTable.keys()):

​    if headerTable[k] < minSup:

​      del(headerTable[k]) # 删除不满足最小支持度的元素

  freqItemSet = set(headerTable.keys()) # 满足最小支持度的频繁项集

  if len(freqItemSet) == 0:

​    return None, None

  for k in headerTable:

​    headerTable[k] = [headerTable[k], None] # element: [count, node]

  

  retTree = treeNode('Null Set', 1, None)

  for tranSet, count in dataSet.items():

​    \# dataSet：[element, count]

​    localD = {}

​    for item in tranSet:

​      if item in freqItemSet: # 过滤，只取该样本中满足最小支持度的频繁项

​        localD[item] = headerTable[item][0] # element : count

​    if len(localD) > 0:

​      \# 根据全局频数从大到小对单样本排序

​      \# orderedItem = [v[0] for v in sorted(localD.iteritems(), key=lambda p:(p[1], -ord(p[0])), reverse=True)]

​      orderedItem = [v[0] for v in sorted(localD.items(), key=lambda p:(p[1], int(p[0])), reverse=True)]

​      \# 用过滤且排序后的样本更新树

​      updateFPtree(orderedItem, retTree, headerTable, count)

  return retTree, headerTable

 

def ascendFPtree(leafNode, prefixPath):

  """

  树的回溯

  @leafNode: 叶子结点

  @prefixPath: 前缀路径索引

  """

  if leafNode.parent != None:

​    prefixPath.append(leafNode.name)

​    ascendFPtree(leafNode.parent, prefixPath)

 

def findPrefixPath(basePat, myHeaderTab):

  """

  找到条件模式基

  @basePat: 模式基

  @myHeaderTab: 链表的头索引表

  """

  treeNode = myHeaderTab[basePat][1] # basePat在FP树中的第一个结点

  condPats = {}

  while treeNode != None:

​    prefixPath = []

​    ascendFPtree(treeNode, prefixPath) # prefixPath是倒过来的，从treeNode开始到根

​    if len(prefixPath) > 1:

​      condPats[frozenset(prefixPath[1:])] = treeNode.count # 关联treeNode的计数

​    treeNode = treeNode.nodeLink # 下一个basePat结点

  return condPats

 

def mineFPtree(inTree, headerTable, minSup, preFix, freqItemList):

  """

  生成我的FP-Tree

  @inTree:

  @headerTable:

  @minSup:

  @preFix: 频繁项

  @ freqItemList: 频繁项所有组合集合 

  """

  \# 最开始的频繁项集是headerTable中的各元素

  bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p:p[1])] # 根据频繁项的总频次排序

  for basePat in bigL: # 对每个频繁项

​    newFreqSet = preFix.copy()

​    newFreqSet.add(basePat)

​    freqItemList.append(newFreqSet)

​    condPattBases = findPrefixPath(basePat, headerTable) # 当前频繁项集的条件模式基

​    myCondTree, myHead = createFPtree(condPattBases, minSup) # 构造当前频繁项的条件FP树

​    if myHead != None:

​      \# print 'conditional tree for: ', newFreqSet

​      \# myCondTree.disp(1)

​      mineFPtree(myCondTree, myHead, minSup, newFreqSet, freqItemList) # 递归挖掘条件FP树

 

def createInitSet(dataSet):

  """

  创建输入格式

  @dataset: 数据集

  """

  retDict={}

  for trans in dataSet:

​    key = frozenset(trans)

​    if key in retDict:

​      retDict[frozenset(trans)] += 1

​    else:

​      retDict[frozenset(trans)] = 1

  return retDict

 

def calSuppData(headerTable, freqItemList, total):

  """

  计算支持度

  @headerTable:

  @freqItemList: 频繁项集

  @total: 总数

  """

  suppData = {}

  for Item in freqItemList:

​    \# 找到最底下的结点

​    Item = sorted(Item, key=lambda x:headerTable[x][0])

​    base = findPrefixPath(Item[0], headerTable)

​    \# 计算支持度

​    support = 0

​    for B in base:

​      if frozenset(Item[1:]).issubset(set(B)):

​        support += base[B]

​    \# 对于根的子结点，没有条件模式基

​    if len(base)==0 and len(Item)==1:

​      support = headerTable[Item[0]][0]

​      

​    suppData[frozenset(Item)] = support/float(total)

  return suppData

 

def aprioriGen(Lk, k):

  retList = []

  lenLk = len(Lk)

  for i in range(lenLk):

​    for j in range(i+1, lenLk):

​      L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]

​      L1.sort(); L2.sort()

​      if L1 == L2: 

​        retList.append(Lk[i] | Lk[j])

  return retList

 

def calcConf(freqSet, H, supportData, br1, minConf=0.7):

  """

  计算置信度，规则评估函数

  @freqSet: 频繁项集，H的超集

  @H: 目标项

  @supportData: 测试

  """

  prunedH = []

  for conseq in H:

​    conf = supportData[freqSet] / supportData[freqSet - conseq]

​    if conf >= minConf:

​      print("{0} --> {1} conf:{2}".format(freqSet - conseq, conseq, conf))

​      br1.append((freqSet - conseq, conseq, conf))

​      prunedH.append(conseq)

  return prunedH

 

def rulesFromConseq(freqSet, H, supportData, br1, minConf=0.7):

  """

  这里H相当于freqSet的子集，在这个函数里面，循环是从子集元素个数由2一直增大到freqSet的元素个数减1

  参数含义同calcConf

  """

  m = len(H[0])

  if len(freqSet) > m+1:

​    Hmp1 = aprioriGen(H, m+1)

​    Hmp1 = calcConf(freqSet, Hmp1, supportData, br1, minConf)

​    if len(Hmp1)>1:

​      rulesFromConseq(freqSet, Hmp1, supportData, br1, minConf)

 

def generateRules(freqItemList, supportData, minConf=0.7):

  """

  关联规则生成主函数

  @L: 频繁集项列表  

  @supportData: 包含频繁项集支持数据的字典 

  @minConf: 最小可信度阈值

  构建关联规则需有大于等于两个的元素

  """

  bigRuleList = []

  for freqSet in freqItemList:

​    H1 = [frozenset([item]) for item in freqSet]

​    if len(freqSet)>1:

​      rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)

​    else:

​      calcConf(freqSet, H1, supportData, bigRuleList, minConf)

  return bigRuleList


 

\# 读取数据

dataset = pd.read_csv('retail.csv', usecols=['items'])

for index, row in dataset.iterrows():

​    dataset.loc[index, 'items'] = row['items'].strip()

dataset = dataset['items'].str.split(" ")

start = time()

initSet = createInitSet(dataset.values)

\# # 用数据集构造FP树，最小支持度5000

myFPtree, myHeaderTab = createFPtree(initSet, 5000)

freqItems = []

mineFPtree(myFPtree, myHeaderTab, 5000, set([]), freqItems)

print("结束搜索，总耗时%s"%(time() - start))

\# for x in freqItems:

\#   print(x)
```

 

\2.  Apriori调用库：

Apriori可以调用库实现：

\# -*- coding: utf-8 -*-

```python
"""

Created on Mon Apr 12 17:11:24 2021

 

@author: Yuetian

"""

 

\# 使用apriori包进行分析

import pandas as pd

from apyori import apriori

dataset = pd.read_csv('retail.csv', usecols=['items'])

def create_dataset(data):

  for index, row in data.iterrows():

​    data.loc[index, 'items'] = row['items'].strip()

  data = data['items'].str.split(" ", expand = True)

  \# 按照list来存储

  output = []

  for i in range(data.shape[0]):

​    output.append([str(data.values[i, j]) for j in range(data.shape[1])])

  return output

 

dataset = create_dataset(dataset)

association_rules = apriori(dataset, min_support = 0.05, min_confidence = 0.7, min_lift = 1.2, min_length = 2)

association_result = list(association_rules)

association_result
```

