import numpy as np


'''
数据加载
'''
def loadDataSet(filePath):
    f = open(filePath)
    dataList = []
    labelList = []
    for line in f.readlines():
        currLine = line.strip().split('\t')
        lineArr = []
        for i in range(21):
            lineArr.append(float(currLine[i]))
        dataList.append(lineArr)
        labelList.append(float(currLine[21]))
    return dataList, labelList


'''
sigmoid函数
'''
def sigmoid(inX):
    return 1.0 / (1 + np.exp(-inX))


'''
随机梯度下降算法
'''
def stocGradAscent(dataList, labelList, numIter=150):
    dataArr = np.array(dataList)
    m, n = np.shape(dataArr)
    weights = np.ones(n)
    for j in range(numIter):
        dataIndex = list(range(m))
        for i in range(m):
            alpha = 4 / (1.0 + j + i) + 0.01  # 步长为动态变化
            rand = int(np.random.uniform(0, len(dataIndex)))
            choseIndex = dataIndex[rand]
            h = sigmoid(np.sum(dataArr[choseIndex] * weights))
            error = h - labelList[choseIndex]
            weights = weights - alpha * error * dataArr[choseIndex]
            del (dataIndex[rand])
    return weights


'''
进行分类
'''
def classifyVector(inX, weights):
    prob = sigmoid(np.sum(inX * weights))
    if prob > 0.5:
        return 1.0
    else:
        return 0.0


'''
在测试集上计算分类精度
'''
def colicTest(trainWeights, testDataList, testLabelList):
    rightCount = 0  # 判断错误的数量
    testCount = len(testDataList)
    for i in range(testCount):
        if int(classifyVector(np.array(testDataList[i]), trainWeights))==int(testLabelList[i]):
            rightCount += 1
    acc = float(rightCount)/testCount
    print("本次的精度为%f" % acc)
    return acc


def main():
    numTests = 10
    errorSum = 0.0
    trainDataList, trainLabelList = loadDataSet("horseColicTraining.txt")
    testDataList, testLabelList = loadDataSet("horseColicTest.txt")
    for i in range(numTests):
        trainWeights = stocGradAscent(trainDataList, trainLabelList, 500)
        errorSum += colicTest(trainWeights, testDataList, testLabelList)
    print("这%d次的平均精度为%f"%(numTests, errorSum/numTests))


if __name__ == '__main__':
    main()
