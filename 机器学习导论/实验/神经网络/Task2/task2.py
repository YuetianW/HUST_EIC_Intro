import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers
from tensorflow.keras import models
from keras.utils import to_categorical
import numpy as np

# 读入数据
file_name = 'train/train_texts.dat'
with open(file_name, 'rb') as f:
    train_texts = pickle.load(f)
file_name = 'test/test_texts.dat'
with open(file_name, 'rb') as f:
    test_texts = pickle.load(f)

train_labals = []
fl = open('train/train_labels.txt')
for line in fl.readlines():
    train_labals.append(line)

# TFIDF向量化
vectorizer = TfidfVectorizer(max_features=10000)
train_vector = vectorizer.fit_transform(train_texts)
print(train_vector.shape)
test_vector = vectorizer.transform(test_texts)
print(test_vector.shape)

one_hot_train_labels = to_categorical(train_labals)

# 定义Sequential类
model = models.Sequential()
# 全连接层，128个节点
model.add(layers.Dense(128, activation='relu', input_shape=(10000,)))
# 全连接层，64个节点
model.add(layers.Dense(64, activation='relu'))
# 全连接层，得到输出
model.add(layers.Dense(20, activation='softmax'))
# loss
model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

#拆分测试集与训练集
X_train, X_test, y_train, y_test = train_test_split(train_vector, one_hot_train_labels, test_size=0.2, random_state=0)
x_test = X_test.toarray()
partial_x_train = X_train.toarray()

history = model.fit(partial_x_train,
                    y_train,
                    epochs=10,
                    batch_size=512,
                    validation_data=(x_test, y_test))

results = model.evaluate(x_test, y_test)

#结果输出：
x_input = test_vector.toarray()
predictions = model.predict(x_input)
out_put = np.argmax(predictions,axis=1)
np.savetxt('result.txt', out_put, fmt='%d', delimiter='\n')


# history = model.fit(partial_x_train,
#                     y_train,
#                     epochs=20,
#                     batch_size=512,
#                     validation_data=(x_test, y_test))
#
# loss = history.history['loss']
# val_loss = history.history['val_loss']
# epochs = range(1, len(loss) + 1)
# plt.plot(epochs, loss, 'bo', label='Training loss')
# plt.plot(epochs, val_loss, 'b', label='Validation loss')
# plt.title('Training and validation loss')
# plt.xlabel('Epochs')
# plt.ylabel('Loss')
# plt.legend()
# plt.show()
#
# plt.clf()
# acc = history.history['accuracy']
# val_acc = history.history['val_accuracy']
# plt.plot(epochs, acc, 'bo', label='Training acc')
# plt.plot(epochs, val_acc, 'b', label='Validation acc')
# plt.title('Training and validation accuracy')
# plt.xlabel('Epochs')
# plt.ylabel('Accuracy')
# plt.legend()
# plt.show()
#



x_input = test_vector.toarray()
predictions = model.predict(x_input)
