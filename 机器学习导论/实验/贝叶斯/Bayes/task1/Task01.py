import numpy as np


def textParse(bigString):
    import re
    listOfTokens=re.split('\W',bigString) #匹配非字母数字下划线
    return [tok.lower() for tok in listOfTokens if len(tok)>2] #若文本中有URL，对其进行切分时，会得到很多词，为避免该情况，限定字符创的长度


#将文档矩阵中的所有词构成词汇表
def creatVocabList(dataset):
    vocabSet=set([])
    for document in dataset:
         vocabSet=vocabSet|set(document)  #两个集合的并集
    return list(vocabSet)


#将某一文档转换成词向量，该向量中所含数值数目与词汇表中词汇数目相同
#词集模型
def setOfWords2Vec(vocabList,inputSet): #参数分别为词汇表，输入文档
    returnVec=[0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            #1表示词向量该位置对应的词汇表中的单词，出现在inpust文档中
            returnVec[vocabList.index(word)]=1
    return returnVec

#将某一文档转换成词向量，该向量中所含数值数目与词汇表中词汇数目相同
#词袋模型
def bagOfWords2Vec(vocabList,inputSet): #参数分别为词汇表，输入文档
    returnVec=[0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]+=1
    return returnVec



#朴素贝叶斯分类器训练函数
#trainMatrix为文档词向量矩阵,
#trainCategory为每篇文档的类标签构成的向量
def trainNB0(trainMatrix,trainCategory):
    numTrainDocs=len(trainMatrix)  #总文档数
    numWords=len(trainMatrix[0])  #所有词的数目
    pAbusive=sum(trainCategory)/float(numTrainDocs)  #侮辱性概率，即P(1)
    p0Num=np.ones(numWords); p1Num=np.ones(numWords)
    p0Deom=2.0; p1Deom=2.0
    for i in range(numTrainDocs):
        if trainCategory[i]==1:
            p1Num+=trainMatrix[i]  #向量相加
            p1Deom+=sum(trainMatrix[i]) #所有垃圾邮件中出现的词条的总计数值
        else:
            p0Num+=trainMatrix[i]
            p0Deom+=sum(trainMatrix[i])
    p1Vect=np.log(p1Num/p1Deom) #在垃圾文档条件下词汇表中单词的出现概率
    p0Vect=np.log(p0Num/p0Deom)
    #pAbusive就是人以文档属于垃圾文档的概率
    return p0Vect,p1Vect,pAbusive



#朴素贝叶斯分类函数
def classifyNB(vec2Classify,p0Vec,p1Vec,pClass): #参数分别为：要分类的向量以及使用trainNB0()计算得到的三个概率
    p1=sum(vec2Classify*p1Vec)+np.log(pClass)
    p0=sum(vec2Classify*p0Vec)+np.log(1-pClass)
    if p1>p0:
        return 1  #表示侮辱性文档
    else:
        return 0
#测试算法：使用朴素贝叶斯交叉验证。同时保存分类模型的词汇表以及三个概率值，避免判断时重复求值
def spamTest():
    docList = []  # 文档（邮件）矩阵
    classList = []  # 类标签列表
    for i in range(1, 26):
        wordlist = textParse(open('spam/{}.txt'.format(str(i))).read())
        docList.append(wordlist)
        classList.append(1)
        wordlist = textParse(open('ham/{}.txt'.format(str(i))).read())
        docList.append(wordlist)
        classList.append(0)
    vocabList = creatVocabList(docList)  # 所有邮件内容的词汇表
    import pickle
    file=open('vocabList.txt',mode='wb')  #存储词汇表
    pickle.dump(vocabList,file)
    file.close()
    # 对需要测试的邮件，根据其词表fileWordList构造向量
    # 随机构建40训练集与10测试集
    trainingSet = list(range(50))
    testSet = []
    for i in range(10):
        randIndex = int(np.random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del (trainingSet[randIndex])
    trainMat = []  # 训练集
    trainClasses = []  # 训练集中向量的类标签列表
    for docIndex in trainingSet:
        # 使用词袋模式构造的向量组成训练集
        trainMat.append(bagOfWords2Vec(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0v,p1v,pAb=trainNB0(trainMat,trainClasses)
    file=open('threeRate.txt',mode='wb') #用以存储分类器的三个概率
    pickle.dump([p0v,p1v,pAb],file)
    file.close()
    errorCount=0
    for docIndex in testSet:
        wordVector=bagOfWords2Vec(vocabList,docList[docIndex])
        if classifyNB(wordVector,p0v,p1v,pAb)!=classList[docIndex]:
            errorCount+=1
    return float(errorCount)/len(testSet)


def fileClassify(filepath):
    import pickle
    fileWordList=textParse(open(filepath,mode='r').read())
    file=open('data/vocabList.txt',mode='rb')
    vocabList=pickle.load(file)
    vocabList=vocabList
    fileWordVec=bagOfWords2Vec(vocabList,fileWordList) #被判断文档的向量
    file=open('data/threeRate.txt',mode='rb')
    rate=pickle.load(file)
    p0v=rate[0];p1v=rate[1];pAb=rate[2]
    return classifyNB(fileWordVec,p0v,p1v,pAb)


if __name__=='__main__':
    erlist = []
    for i in range(10):
        resnow = spamTest()
        erlist.append(spamTest())
        print('朴素贝叶斯分类的错误率为：{}'.format(resnow))  #测试算法的错误率
    arv = np.mean(erlist)
    print('平均值为：{}'.format(arv))
    # filepath=input('输入需判断的邮件路径')
    # #判断某一路径下的邮件是否为垃圾邮件
    # if fileClassify('spam/1.txt')==1:
    #     print('垃圾邮件')
    # else:
    #     print('非垃圾邮件')
