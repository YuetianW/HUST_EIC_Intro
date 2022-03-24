# 顺序模型
from keras import Sequential
# 网络，卷积，扁平化，Dropout
from keras.layers import Dense, Conv2D, MaxPooling2D, UpSampling2D, Dropout, Flatten
# one hot
from keras import utils
# 优化器
from keras.optimizers import Adam  # 收敛速度快
# Mnist数据集
from keras.datasets import mnist
# CIFAR-10数据集
from keras.datasets import cifar10

import numpy as np
import matplotlib.pyplot as plt


# 返回mnist归一化以后的数据
def get_data(dataset):
    # 导入数据集
    if dataset == 'mnist':
        (x_train, y_train), (x_test, y_test) = mnist.load_data()
    if dataset == 'cifar10':
        (x_train, y_train), (x_test, y_test) = cifar10.load_data()

    # 打印显示原始数据维度
    print("原始数据大小：")
    print("x_train的大小为：", x_train.shape)
    print("y_train的大小为：", y_train.shape)
    print("x_test的大小为：", x_test.shape)
    print("y_test的大小为：", y_test.shape)

    # 转化数据使得一行为一副图像
    x_train = x_train.reshape(x_train.shape[0], -1).astype("float64")
    x_test = x_test.reshape(x_test.shape[0], -1).astype("float64")

    # 将图像除以255进行像素值归一化
    x_train /= 255
    x_test /= 255

    # 将y_train与y_test转化为“one hot”形式
    y_train = utils.to_categorical(y_train)
    y_test = utils.to_categorical(y_test)

    # 打印转化后数据大小
    print("\n转化后数据大小：")
    print("x_train的大小为：", x_train.shape)
    print("y_train的大小为：", y_train.shape)
    print("x_test的大小为：", x_test.shape)
    print("y_test的大小为：", y_test.shape)

    return x_train, y_train, x_test, y_test


# 定义AlexNet网络，该定义处理深度为1，即灰度图像
def AlexNet(x_train, y_train, x_test, y_test, rows, cols, depth, MAX_LOOP=3):
    # 将x_train与x_test转化为n_samples * rows * cols * depth大小
    x_train = x_train.reshape(-1, rows, cols, depth)
    x_test = x_test.reshape(-1, rows, cols, depth)

    ####### 建立网络 ######
    # 顺序模型
    model = Sequential()

    # 卷积，池化部分
    model.add(Conv2D(96, (11, 11), strides=(4, 4), input_shape=(rows, cols, depth), padding='same',
                     activation='relu', kernel_initializer='uniform'))
    model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2), padding='same', data_format='channels_last'))
    model.add(Conv2D(256, (5, 5), strides=(1, 1), padding='same',
                     activation='relu', kernel_initializer='uniform'))
    model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2), padding='same', data_format='channels_last'))
    model.add(Conv2D(384, (3, 3), strides=(1, 1), padding='same',
                     activation='relu', kernel_initializer='uniform'))
    model.add(Conv2D(384, (3, 3), strides=(1, 1), padding='same',
                     activation='relu', kernel_initializer='uniform'))
    model.add(Conv2D(256, (3, 3), strides=(1, 1), padding='same',
                     activation='relu', kernel_initializer='uniform'))
    model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2), padding='same', data_format='channels_last'))

    # 扁平化
    model.add(Flatten())

    # 全连接部分
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(10, activation='softmax'))
    ######################

    # 网络结构展示
    print('\n网络结构：')
    model.summary()
    utils.plot_model(model, to_file='model.png', show_shapes=True)

    # 设置优化器
    adam = Adam()

    # 整合模型
    model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])

    # 开始训练
    my_batch_size = round(x_train.shape[0] * 0.001)  # 定义batch_size大小
    print("\n开始训练：")
    history = model.fit(x_train, y_train, validation_data=(x_test, y_test), batch_size=my_batch_size, epochs=MAX_LOOP)
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    epochs = range(1, MAX_LOOP + 1)
    plt.plot(epochs, acc, 'b', label='Training acc')
    plt.plot(epochs, val_acc, 'r', label='Validation acc')
    plt.xlabel('Epochs')
    plt.ylabel('acc')
    plt.ylim(0.5, 1.1)
    plt.legend()
    plt.show()

    # 评价模型
    print("\n评价模型：")
    final_loss, final_accuracy = model.evaluate(x_test, y_test)
    print("loss= ", final_loss)
    print("accuracy= ", final_accuracy)

    return model


# 抽取一张图像进行预测展示
def test_AlexNet_model(model, x_test, rows, cols, depth):
    # 选取一个测试集合图像的序号
    dex = np.random.randint(0, x_test.shape[0] - 1)
    # 获得该序号的图像
    img = x_test[dex, :].reshape(rows, cols, depth)
    # 利用模型进行预测
    y_predict = np.argmax(model.predict(img.reshape(1, rows, cols, depth)))

    # 显示原图像，打印预测结果
    print("\n随机抽取测试集图像进行预测：")
    print("测试集图像序号为：", dex)
    print("原图像为：")
    if depth == 1:
        plt.imshow(img.squeeze(), cmap='gray')
        plt.show()
    else:
        plt.imshow(img, cmap='gray')
        plt.show()
    print("原图像标签为：", np.argmax(y_test[dex]))
    print("模型预测结果为：", y_predict)


# 设置图像大小，及深度
rows = 28
cols = 28
depth = 1

# 调用自定义函数，获取MNIST数据
x_train, y_train, x_test, y_test = get_data('mnist')

# 调用自定义“AlexNet”网络进行训练
model = AlexNet(x_train, y_train, x_test, y_test, rows, cols, depth,MAX_LOOP= 10)

# 随机测试一个测试集图像
test_AlexNet_model(model, x_test, rows, cols, depth)

model.save('AlexNet_mnist.h5')