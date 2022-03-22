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
        self.name = nameValue  # 存放结点名字
        self.count = numOccur  # 计数器
        self.nodeLink = None  # 连接相似结点
        self.parent = parentNode  # 存放父节点，用于回溯
        self.children = {}  # 存放子节点

    def inc(self, numOccur):
        self.count += numOccur

    def disp(self, ind=1):
        # 输出调试用
        print('  '*ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind+1)

def updateHeader(nodeToTest, targetNode):
    """
    设置头结点
    @nodeToTest: 测试结点
    @targetNode: 目标结点
    """
    while nodeToTest.nodeLink != None:
        nodeToTest = nodeToTest.nodeLink
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
        # 判断items的第一个结点是否已作为子结点
        inTree.children[items[0]].inc(count)
    else:
        # 创建新的分支
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    # 递归
    if len(items) > 1:
        updateFPtree(items[1::], inTree.children[items[0]], headerTable, count)

def createFPtree(dataSet, minSup=1):
    """
    建立FP-Tree
    @dataset: 数据集
    @minSup: 最小支持度
    """
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    for k in list(headerTable.keys()):
        if headerTable[k] < minSup:
            del(headerTable[k]) # 删除不满足最小支持度的元素
    freqItemSet = set(headerTable.keys()) # 满足最小支持度的频繁项集
    if len(freqItemSet) == 0:
        return None, None
    for k in headerTable:
        headerTable[k] = [headerTable[k], None] # element: [count, node]
    
    retTree = treeNode('Null Set', 1, None)
    for tranSet, count in dataSet.items():
        # dataSet：[element, count]
        localD = {}
        for item in tranSet:
            if item in freqItemSet: # 过滤，只取该样本中满足最小支持度的频繁项
                localD[item] = headerTable[item][0] # element : count
        if len(localD) > 0:
            # 根据全局频数从大到小对单样本排序
            # orderedItem = [v[0] for v in sorted(localD.iteritems(), key=lambda p:(p[1], -ord(p[0])), reverse=True)]
            orderedItem = [v[0] for v in sorted(localD.items(), key=lambda p:(p[1], int(p[0])), reverse=True)]
            # 用过滤且排序后的样本更新树
            updateFPtree(orderedItem, retTree, headerTable, count)
    return retTree, headerTable

def ascendFPtree(leafNode, prefixPath):
    """
    树的回溯
    @leafNode: 叶子结点
    @prefixPath: 前缀路径索引
    """
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendFPtree(leafNode.parent, prefixPath)

def findPrefixPath(basePat, myHeaderTab):
    """
    找到条件模式基
    @basePat: 模式基
    @myHeaderTab: 链表的头索引表
    """
    treeNode = myHeaderTab[basePat][1] # basePat在FP树中的第一个结点
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendFPtree(treeNode, prefixPath) # prefixPath是倒过来的，从treeNode开始到根
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count # 关联treeNode的计数
        treeNode = treeNode.nodeLink # 下一个basePat结点
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
    # 最开始的频繁项集是headerTable中的各元素
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p:p[1])] # 根据频繁项的总频次排序
    for basePat in bigL: # 对每个频繁项
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable) # 当前频繁项集的条件模式基
        myCondTree, myHead = createFPtree(condPattBases, minSup) # 构造当前频繁项的条件FP树
        if myHead != None:
            # print 'conditional tree for: ', newFreqSet
            # myCondTree.disp(1)
            mineFPtree(myCondTree, myHead, minSup, newFreqSet, freqItemList) # 递归挖掘条件FP树

def createInitSet(dataSet):
    """
    创建输入格式
    @dataset: 数据集
    """
    retDict={}
    for trans in dataSet:
        key = frozenset(trans)
        if key in retDict:
            retDict[frozenset(trans)] += 1
        else:
            retDict[frozenset(trans)] = 1
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
        # 找到最底下的结点
        Item = sorted(Item, key=lambda x:headerTable[x][0])
        base = findPrefixPath(Item[0], headerTable)
        # 计算支持度
        support = 0
        for B in base:
            if frozenset(Item[1:]).issubset(set(B)):
                support += base[B]
        # 对于根的子结点，没有条件模式基
        if len(base)==0 and len(Item)==1:
            support = headerTable[Item[0]][0]
            
        suppData[frozenset(Item)] = support/float(total)
    return suppData

def aprioriGen(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]
            L1.sort(); L2.sort()
            if L1 == L2: 
                retList.append(Lk[i] | Lk[j])
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
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        if conf >= minConf:
            print("{0} --> {1} conf:{2}".format(freqSet - conseq, conseq, conf))
            br1.append((freqSet - conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH

def rulesFromConseq(freqSet, H, supportData, br1, minConf=0.7):
    """
    这里H相当于freqSet的子集，在这个函数里面，循环是从子集元素个数由2一直增大到freqSet的元素个数减1
    参数含义同calcConf
    """
    m = len(H[0])
    if len(freqSet) > m+1:
        Hmp1 = aprioriGen(H, m+1)
        Hmp1 = calcConf(freqSet, Hmp1, supportData, br1, minConf)
        if len(Hmp1)>1:
            rulesFromConseq(freqSet, Hmp1, supportData, br1, minConf)

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
        H1 = [frozenset([item]) for item in freqSet]
        if len(freqSet)>1:
            rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
        else:
            calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList



# 读取数据
dataset = pd.read_csv('retail.csv', usecols=['items'])
for index, row in dataset.iterrows():
        dataset.loc[index, 'items'] = row['items'].strip()
dataset = dataset['items'].str.split(" ")
start = time()
initSet = createInitSet(dataset.values)
# # 用数据集构造FP树，最小支持度5000
myFPtree, myHeaderTab = createFPtree(initSet, 5000)
freqItems = []
mineFPtree(myFPtree, myHeaderTab, 5000, set([]), freqItems)
print("结束搜索，总耗时%s"%(time() - start))
# for x in freqItems:
#     print(x)
