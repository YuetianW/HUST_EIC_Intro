from keras.datasets import imdb
from sklearn.tree import DecisionTreeClassifier
import numpy as np

(train_data, train_labels), (test_data_f, test_labels_f) = imdb.load_data(num_words=10000)
# 取出数据集
with open("test/test_data.txt", "rb") as fr:
    test_data_n = [inst.decode().strip().split(' ') for inst in fr.readlines()]
    test_data = [[int(element) for element in line] for line in test_data_n]
test_data = np.array(test_data)

# 将某条评论解码为英文单词
word_index = imdb.get_word_index()  # word_index是一个将单词映射为整数索引的字典
reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])

# 键值颠倒，将整数索引映射为单词
decode_review = ' '.join(
    [reverse_word_index.get(i - 3, '?') for i in train_data[0]]
)  # 将评论解码，注意，索引减去了3，因为0,1,2是为padding填充，"start sequence"序列开始，"unknow"未知词分别保留的索引


# 将整数序列编码为二进制矩阵
def vectorize_sequences(sequences, dimension=10000):
    results = np.zeros((len(sequences), dimension))  # 创建一个形状为(len(sequences), dimension)的矩阵
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1  # 将results[i]的指定索引设为 1
    return results


x_train = vectorize_sequences(train_data)
x_test = vectorize_sequences(test_data)

# 标签向量化
y_train = np.asarray(train_labels).astype('float32')
# y_test = np.asarray(test_labels).astype('float32')
# 建立决策树  在此全部为默认参数了  主要参数criterion可选‘gini'或'entropy'作为生成树依据,max_deoth可以决定树的深度，max_leaf_nodes限制最大叶子树
decision_tree_classifier = DecisionTreeClassifier()
decision_tree_classifier.fit(x_train, y_train)
decision_tree_output = decision_tree_classifier.predict(x_test)
des = decision_tree_output.astype(int)
np.savetxt('Text3_result.txt', des, fmt='%d', delimiter='\n')
print(decision_tree_output)



# score = accuracy_score(y_test, decision_tree_output)
# print(score)