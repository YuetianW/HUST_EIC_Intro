

# **《机器学习导论》实验报告

[TOC]



# 编程作业：SVM

## 实验原理：

### **序列最小优化算法(SMO)**

参考：

[支持向量机(SVM)——SMO算法 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/32152421)

[机器学习算法实践-SVM中的SMO算法 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/29212107)

​	

#### **SMO算法介绍**

SMO的思想类似坐标上升算法，我们需要优化一系列的αα的值，我们每次选择尽量少的![[公式]](https://www.zhihu.com/equation?tex=%5Calpha)来优化，不断迭代直到函数收敛到最优值。

来到SVM的对偶问题上，对偶形式:

![[公式]](https://www.zhihu.com/equation?tex=arg+%5Cmax+%5Climits_%7B%5Calpha%7D+%5Csum_%7Bi%3D1%7D%5E%7BN%7D+%5Calpha_%7Bi%7D+-+%5Cfrac%7B1%7D%7B2%7D%5Csum_%7Bi%3D1%7D%5E%7BN%7D%5Csum_%7Bj%3D1%7D%5E%7BN%7Dy_%7Bi%7Dy_%7Bj%7D%5Calpha_%7Bi%7D%5Calpha_%7Bj%7D%5Clangle+x_%7Bi%7D%2C+x_%7Bj%7D+%5Crangle)

subject to![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7Bi%7D+%5Cge+0),![[公式]](https://www.zhihu.com/equation?tex=%5Csum_%7Bi%3D1%7D%5E%7BN%7D%5Calpha_%7Bi%7Dy_%7Bi%7D%3D0)

其中我们需要对![[公式]](https://www.zhihu.com/equation?tex=%28%5Calpha_%7B1%7D%2C+%5Calpha_%7B2%7D%2C+%E2%80%A6%2C+%5Calpha_%7BN%7D%29)进行优化，但是这个凸二次优化问题的其他求解算法的复杂度很高，但是Platt提出的SMO算法可以高效的求解上述对偶问题，他把原始问题的求解![[公式]](https://www.zhihu.com/equation?tex=N)个参数二次规划问题分解成多个二次规划问题求解，每个字问题只需要求解2各参数，节省了时间成本和内存需求。

与坐标上升算法不同的是，我们在SMO算法中我们每次需要选择**一对**变量![[公式]](https://www.zhihu.com/equation?tex=%28%5Calpha_i%2C+%5Calpha_j%29), 因为在SVM中，我们的![[公式]](https://www.zhihu.com/equation?tex=%5Calpha)并不是完全独立的，而是具有约束的:

![[公式]](https://www.zhihu.com/equation?tex=%5Csum_%7Bi%3D1%7D%5E%7BN%7D%5Calpha_%7Bi%7Dy_%7Bi%7D+%3D+0)

因此一个![[公式]](https://www.zhihu.com/equation?tex=%5Calpha)改变，另一个也要随之变化以满足条件。

#### **SMO算法原理**

**获得没有修剪的原始解**

假设我们选取的两个需要优化的参数为![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_1%2C+%5Calpha_2), 剩下的![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7B3%7D%2C+%5Calpha_%7B4%7D%2C+%E2%80%A6%2C+%5Calpha_%7BN%7D)则固定，作为常数处理。将SVM优化问题进行展开就可以得到(把与![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7B1%7D%2C+%5Calpha_%7B2%7D)无关的项合并成常数项![[公式]](https://www.zhihu.com/equation?tex=C)):

![[公式]](https://www.zhihu.com/equation?tex=W%28%5Calpha_%7B1%7D%2C+%5Calpha_%7B2%7D%29+%3D+%5Calpha_%7B1%7D+%2B+%5Calpha_%7B2%7D+-+%5Cfrac%7B1%7D%7B2%7DK_%7B1%2C1%7Dy_%7B1%7D%5E%7B2%7D%5Calpha_%7B1%7D%5E%7B2%7D+-+%5Cfrac%7B1%7D%7B2%7DK_%7B2%2C2%7Dy_%7B2%7D%5E%7B2%7D%5Calpha_%7B2%7D%5E%7B2%7D+-+K_%7B1%2C2%7Dy_%7B1%7Dy_%7B2%7D%5Calpha_%7B1%7D%5Calpha_%7B2%7D+-+y_%7B1%7D%5Calpha_%7B1%7D%5Csum_%7Bi%3D3%7D%5E%7BN%7D%5Calpha_%7Bi%7Dy_%7Bi%7DK_%7Bi%2C1%7D+-+y_%7B2%7D%5Calpha_%7B2%7D%5Csum_%7Bi%3D3%7D%5E%7BN%7D%5Calpha_%7Bi%7Dy_%7Bi%7DK_%7Bi%2C+2%7D+%2B+C)

于是就是一个二元函数的优化:

![[公式]](https://www.zhihu.com/equation?tex=arg+%5Cmax+%5Climits_%7B%5Calpha_%7B1%7D%2C+%5Calpha_%7B2%7D%7D+W%28%5Calpha_%7B1%7D%2C+%5Calpha_%7B2%7D%29)

根据约束条件![[公式]](https://www.zhihu.com/equation?tex=%5Csum_%7Bi%3D1%7D%5E%7BN%7D%5Calpha_%7Bi%7Dy_%7Bi%7D+%3D+0)可以得到![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_1)与![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_2)的关系:

![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7B1%7Dy_%7B1%7D+%2B+%5Calpha_%7B2%7Dy_%7B2%7D+%3D+-%5Csum_%7Bi%3D3%7D%5E%7BN%7D%5Calpha_%7Bi%7Dy_%7Bi%7D+%3D+%5Czeta)

两边同时乘上![[公式]](https://www.zhihu.com/equation?tex=y_1), 由于![[公式]](https://www.zhihu.com/equation?tex=y_%7Bi%7Dy_%7Bi%7D+%3D+1)得到:

![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7B1%7D+%3D+%5Czeta+y_%7B1%7D+-+%5Calpha_%7B2%7Dy_%7B1%7Dy_%7B2%7D)

令![[公式]](https://www.zhihu.com/equation?tex=v_%7B1%7D+%3D+%5Csum_%7Bi%3D3%7D%5E%7BN%7D%5Calpha_%7Bi%7Dy_%7Bi%7DK_%7Bi%2C+1%7D),![[公式]](https://www.zhihu.com/equation?tex=v_%7B2%7D+%3D+%5Csum_%7Bi%3D3%7D%5E%7BN%7D%5Calpha_%7Bi%7Dy_%7Bi%7DK_%7Bi%2C+2%7D)，![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_1)的表达式代入得到:

![[公式]](https://www.zhihu.com/equation?tex=W%28%5Calpha_%7B2%7D%29+%3D+-%5Cfrac%7B1%7D%7B2%7DK_%7B1%2C+1%7D%28%5Czeta+-+%5Calpha_%7B2%7Dy_%7B2%7D%29%5E%7B2%7D+-+%5Cfrac%7B1%7D%7B2%7DK_%7B2%2C+2%7D%5Calpha_%7B2%7D%5E%7B2%7D+-+y_%7B2%7D%28%5Czeta+-+%5Calpha_%7B2%7Dy_%7B2%7D%29%5Calpha_%7B2%7DK_%7B1%2C+2%7D+-+v_%7B1%7D%28%5Czeta+-+%5Calpha_%7B2%7Dy_%7B2%7D%29+-+v_%7B2%7Dy_%7B2%7D%5Calpha_%7B2%7D+%2B+%5Calpha_%7B1%7D+%2B+%5Calpha_%7B2%7D+%2B+C)

后面我们需要对这个一元函数进行求极值，![[公式]](https://www.zhihu.com/equation?tex=W)对![[公式]](https://www.zhihu.com/equation?tex=%5Calpha)的一阶导数为0得到:

![[公式]](https://www.zhihu.com/equation?tex=%5Cfrac%7B%5Cpartial%7BW%28%5Calpha_%7B2%7D%29%7D%7D%7B%5Cpartial%7B%5Calpha_%7B2%7D%7D%7D+%3D+-%28K_%7B1%2C+1%7D+%2B+K_%7B2%2C+2%7D+-+2K_%7B1%2C+2%7D%29%5Calpha_%7B2%7D+%2B+K_%7B1%2C+1%7D%5Czeta+y_%7B2%7D+-+K_%7B1%2C+2%7D%5Czeta+y_%7B2%7D+%2B+v_%7B1%7Dy_%7B2%7D+-+v_%7B2%7Dy_%7B2%7D+-+y_%7B1%7Dy_%7B2%7D+%2B+y_%7B2%7D%5E%7B2%7D+%3D+0)

下面我们稍微对上式进行下变形，使得![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7B2%7D%5E%7Bnew%7D)能够用更新前的![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7B2%7D%5E%7Bold%7D)表示，而不是使用不方便计算的![[公式]](https://www.zhihu.com/equation?tex=%5Czeta)。

因为SVM对数据点的预测值为:![[公式]](https://www.zhihu.com/equation?tex=f%28x%29+%3D+%5Csum_%7Bi%3D1%7D%5E%7BN%7D%5Calpha_%7Bi%7Dy_%7Bi%7D+K%28x_%7Bi%7D%2C+x%29+%2B+b)

则![[公式]](https://www.zhihu.com/equation?tex=v_1)以及![[公式]](https://www.zhihu.com/equation?tex=v_2)的值可以表示成:

![[公式]](https://www.zhihu.com/equation?tex=v_%7B1%7D+%3D+%5Csum_%7Bi%3D3%7D%5E%7BN%7D%5Calpha_%7Bi%7Dy_%7Bi%7DK_%7B1%2C+i%7D+%3D+f%28x_%7B1%7D%29+-+%5Calpha_%7B1%7Dy_%7B1%7DK_%7B1%2C+1%7D+-+%5Calpha_%7B2%7Dy_%7B2%7DK_%7B1%2C+2%7D+-+b)

![[公式]](https://www.zhihu.com/equation?tex=v_%7B2%7D+%3D+%5Csum_%7Bi%3D3%7D%5E%7BN%7D%5Calpha_%7Bi%7Dy_%7Bi%7DK_%7B2%2C+i%7D+%3D+f%28x_%7B2%7D%29+-+%5Calpha_%7B1%7Dy_%7B1%7DK_%7B1%2C+2%7D+-+%5Calpha_%7B2%7Dy_%7B2%7DK_%7B2%2C+2%7D+-+b)

已知![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7B1%7D+%3D+%28%5Czeta+-+%5Calpha_%7B2%7Dy_%7B2%7D%29y_%7B2%7D), 可得到:

![[公式]](https://www.zhihu.com/equation?tex=v_%7B1%7D+-+v_%7B2%7D+%3D+f%28x_%7B1%7D%29+-+f%28x_%7B2%7D%29+-+K_%7B1%2C+1%7D%5Czeta+%2B+K_%7B1%2C+2%7D%5Czeta+%2B+%28K_%7B1%2C+1%7D+%2B+K_%7B2%2C+2%7D+-+2K_%7B1%2C+2%7D%29%5Calpha_%7B2%7Dy_%7B2%7D)

将![[公式]](https://www.zhihu.com/equation?tex=v_%7B1%7D+-+v_%7B2%7D)的表达式代入到![[公式]](https://www.zhihu.com/equation?tex=%5Cfrac%7B%5Cpartial%7BW%28%5Calpha_%7B2%7D%29%7D%7D%7B%5Cpartial%7B%5Calpha_%7B2%7D%7D%7D)中可以得到:![[公式]](https://www.zhihu.com/equation?tex=%5Cfrac%7B%5Cpartial%7BW%28%5Calpha_%7B2%7D%29%7D%7D%7B%5Cpartial%7B%5Calpha_%7B2%7D%7D%7D+%3D+-%28K_%7B1%2C+1%7D%29+%2B+K_%7B2%2C+2%7D+-+2K_%7B1%2C+2%7D%29%5Calpha_%7B2%7D%5E%7Bnew%7D+%2B%28K_%7B1%2C+1%7D%29+%2B+K_%7B2%2C+2%7D+-+2K_%7B1%2C+2%7D%29%5Calpha_%7B2%7D%5E%7Bold%7D+%2B+y_%7B2%7D%5Cleft%5B+y_%7B2%7D+-+y_%7B1%7D+%2B+f%28x_%7B1%7D%29+-+f%28x_%7B2%7D%29+%5Cright%5D)

我们记![[公式]](https://www.zhihu.com/equation?tex=E_i)为SVM预测值与真实值的误差:![[公式]](https://www.zhihu.com/equation?tex=E_%7Bi%7D+%3D+f%28x_%7Bi%7D%29+-+y_%7Bi%7D)

令![[公式]](https://www.zhihu.com/equation?tex=%5Ceta+%3D+K_%7B1%2C+1%7D+%2B+K_%7B2%2C+2%7D+-+2K_%7B1%2C+2%7D)得到最终的一阶导数表达式:

![[公式]](https://www.zhihu.com/equation?tex=%5Cfrac%7B%5Cpartial%7BW%28%5Calpha_%7B2%7D%29%7D%7D%7B%5Cpartial%7B%5Calpha_%7B2%7D%7D%7D+%3D+-%5Ceta+%5Calpha_%7B2%7D%5E%7Bnew%7D+%2B+%5Ceta+%5Calpha_%7B2%7D%5E%7Bold%7D+%2B+y_%7B2%7D%28E_%7B1%7D+-+E_%7B2%7D%29+%3D+0)

得到:

![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7B2%7D%5E%7Bnew%7D+%3D+%5Calpha_%7B2%7D%5E%7Bold%7D+%2B+%5Cfrac%7By_%7B2%7D%28E_%7B1%7D+-+E_%7B2%7D%29%7D%7B%5Ceta%7D)

这样我们就得到了通过旧的![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_2)获取新的![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_2)的表达式,![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7B1%7D%5E%7Bnew%7D)便可以通过![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7B2%7D%5E%7Bnew%7D)得到。

**对原始解进行修剪**

上面我们通过对一元函数求极值的方式得到的最优![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7Bi%7D%2C+%5Calpha_%7Bj%7D)是未考虑约束条件下的最优解，我们便更正我们上部分得到的![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7B2%7D%5E%7Bnew%7D)为![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7B2%7D%5E%7Bnew%2C+unclipped%7D), 即:

![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7B2%7D%5E%7Bnew%2C+unclipped%7D+%3D+%5Calpha_%7B2%7D%5E%7Bold%7D+%2B+%5Cfrac%7By_%7B2%7D%28E_%7B1%7D+-+E_%7B2%7D%29%7D%7B%5Ceta%7D)

但是在SVM中我们的![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_i)是有约束的，即:

![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7B1%7Dy_%7B1%7D+%2B+%5Calpha_%7B2%7Dy_%7B2%7D+%3D+-%5Csum_%7Bi%3D3%7D%5E%7BN%7D%5Calpha_%7Bi%7Dy_%7Bi%7D+%3D+%5Czeta)

![[公式]](https://www.zhihu.com/equation?tex=0+%5Cle+%5Calpha_%7Bi%7D+%5Cle+C)

此约束为方形约束(Bosk constraint), 在二维平面中我们可以看到这是个限制在方形区域中的直线（见下图）。



![img](https://pic3.zhimg.com/80/v2-449670775bab3c385b5e5930fc6d2caa_1440w.png)

(如左图) 当![[公式]](https://www.zhihu.com/equation?tex=y_%7B1%7D+%5Cne+y_%7B2%7D)时，线性限制条件可以写成:![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7B1%7D+-+%5Calpha_%7B2%7D+%3D+k)，根据![[公式]](https://www.zhihu.com/equation?tex=k)的正负可以得到不同的上下界，因此统一表示成:

- - 下界:![[公式]](https://www.zhihu.com/equation?tex=L+%3D+%5Cmax%280%2C+%5Calpha_%7B2%7D%5E%7Bold%7D+-+%5Calpha_%7B1%7D%5E%7Bold%7D%29)
  - 上界:![[公式]](https://www.zhihu.com/equation?tex=H+%3D+%5Cmin%28C%2C+C+%2B+%5Calpha_%7B2%7D%5E%7Bold%7D+-+%5Calpha_%7B1%7D%5E%7Bold%7D%29)

(如右图) 当![[公式]](https://www.zhihu.com/equation?tex=y_%7B1%7D+%3D+y_%7B2%7D)时，限制条件可写成:![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7B1%7D+%2B+%5Calpha_%7B2%7D+%3D+k), 上下界表示成:

- - 下界:![[公式]](https://www.zhihu.com/equation?tex=L+%3D+%5Cmax%280%2C+%5Calpha_%7B1%7D%5E%7Bold%7D+%2B+%5Calpha_%7B2%7D%5E%7Bold%7D+-+C%29)
  - 上界:![[公式]](https://www.zhihu.com/equation?tex=H+%3D+%5Cmin%28C%2C+%5Calpha_%7B2%7D%5E%7Bold%7D+%2B+%5Calpha_%7B1%7D%5E%7Bold%7D%29)

根据得到的上下界，我们可以得到修剪后的![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7B2%7D%5E%7Bnew%7D):

![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7B2%7D%5E%7Bnew%7D+%3D+%5Cbegin%7Bcases%7D+H+%26+%5Calpha_%7B2%7D%5E%7Bnew%2C+unclipped%7D+%3E+H+%5C%5C+%5Calpha_%7B2%7D%5E%7Bnew%2C+unclipped%7D+%26+L+%5Cle+%5Calpha_%7B2%7D%5E%7Bnew%2C+unclipped%7D+%5Cle+H+%5C%5C+L+%26+%5Calpha_%7B2%7D%5E%7Bnew%2C+unclipped%7D+%3C+L+%5Cend%7Bcases%7D)

得到了![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7B2%7D%5E%7Bnew%7D)我们便可以根据![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7B1%7D%5E%7Bold%7Dy_%7B1%7D+%2B+%5Calpha_%7B2%7D%5E%7Bold%7Dy_%7B2%7D+%3D+%5Calpha_%7B1%7D%5E%7Bnew%7Dy_%7B1%7D+%2B+%5Calpha_%7B2%7D%5E%7Bnew%7Dy_%7B2%7D)得到![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7B1%7D%5E%7Bnew%7D):

![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7B1%7D%5E%7Bnew%7D+%3D+%5Calpha_%7B1%7D%5E%7Bold%7D+%2B+y_%7B1%7Dy_%7B2%7D%28%5Calpha_%7B2%7D%5E%7Bold%7D+-+%5Calpha_%7B2%7D%5E%7Bnew%7D%29)



OK， 这样我们就知道如何将选取的一对![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7Bi%7D%2C+%5Calpha_%7Bj%7D)进行优化更新了。

**更新阈值b**

当我们更新了一对![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7Bi%7D%2C+%5Calpha_%7Bj%7D)之后都需要重新计算阈值![[公式]](https://www.zhihu.com/equation?tex=b)，因为![[公式]](https://www.zhihu.com/equation?tex=b)关系到我们![[公式]](https://www.zhihu.com/equation?tex=f%28x%29)的计算，关系到下次优化的时候误差![[公式]](https://www.zhihu.com/equation?tex=E_i)的计算。

为了使得被优化的样本都满足KKT条件，

当![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7B1%7D%5E%7Bnew%7D)不在边界，即![[公式]](https://www.zhihu.com/equation?tex=0+%3C+%5Calpha_%7B1%7D%5E%7Bnew%7D+%3C+C), 根据KKT条件可知相应的数据点为支持向量，满足![[公式]](https://www.zhihu.com/equation?tex=y_%7B1%7D%28w%5E%7BT%7D+%2B+b%29+%3D+1), 两边同时乘上![[公式]](https://www.zhihu.com/equation?tex=y_1)得到![[公式]](https://www.zhihu.com/equation?tex=%5Csum_%7Bi%3D1%7D%5E%7BN%7D%5Calpha_%7Bi%7Dy_%7Bi%7DK_%7Bi%2C+1%7D+%2B+b+%3D+y_%7B1%7D), 进而得到![[公式]](https://www.zhihu.com/equation?tex=b_%7B1%7D%5E%7Bnew%7D)的值:

![[公式]](https://www.zhihu.com/equation?tex=b_%7B1%7D%5E%7Bnew%7D+%3D+y_%7B1%7D+-+%5Csum_%7Bi%3D3%7D%5E%7BN%7D%5Calpha_%7Bi%7Dy_%7Bi%7DK_%7Bi%2C+1%7D+-+%5Calpha_%7B1%7D%5E%7Bnew%7Dy_%7B1%7DK_%7B1%2C+1%7D+-+%5Calpha_%7B2%7D%5E%7Bnew%7Dy_%7B2%7DK_%7B2%2C+1%7D)

其中上式的前两项可以写成:

![[公式]](https://www.zhihu.com/equation?tex=y_%7B1%7D+-+%5Csum_%7Bi%3D3%7D%5E%7BN%7D%5Calpha_%7Bi%7Dy_%7Bi%7DK_%7Bi%2C+1%7D+%3D+-E_%7B1%7D+%2B+%5Calpha_%7B1%7D%5E%7Bold%7Dy_%7B1%7DK_%7B1%2C+1%7D+%2B+%5Calpha_%7B2%7D%5E%7Bold%7Dy_%7B2%7DK_%7B2%2C+1%7D+%2B+b%5E%7Bold%7D)

当![[公式]](https://www.zhihu.com/equation?tex=0+%3C+%5Calpha_%7B2%7D%5E%7Bnew%7D+%3C+C), 可以得到bnew2b2new的表达式(推导同上):

![[公式]](https://www.zhihu.com/equation?tex=b_%7B2%7D%5E%7Bnew%7D+%3D+-E_%7B2%7D+-+y_%7B1%7DK_%7B1%2C+2%7D%28%5Calpha_%7B1%7D%5E%7Bnew%7D+-+%5Calpha_%7B1%7D%5E%7Bold%7D%29+-+y_%7B2%7DK_%7B2%2C+2%7D%28%5Calpha_%7B2%7D%5E%7Bnew%7D+-+%5Calpha_%7B2%7D%5E%7Bold%7D%29+%2B+b%5E%7Bold%7D)

当![[公式]](https://www.zhihu.com/equation?tex=b_1)和![[公式]](https://www.zhihu.com/equation?tex=b_2)都有效的时候他们是相等的, 即![[公式]](https://www.zhihu.com/equation?tex=b%5E%7Bnew%7D+%3D+b_%7B1%7D%5E%7Bnew%7D+%3D+b_%7B2%7D%5E%7Bnew%7D)。

当两个乘子![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7B1%7D%2C+%5Calpha_%7B2%7D)都在边界上，且![[公式]](https://www.zhihu.com/equation?tex=L+%5Cne+H)时，![[公式]](https://www.zhihu.com/equation?tex=b1%2C+b2)之间的值就是和KKT条件一直的阈值。SMO选择他们的中点作为新的阈值:

![[公式]](https://www.zhihu.com/equation?tex=b%5E%7Bnew%7D+%3D+%5Cfrac%7Bb_%7B1%7D%5E%7Bnew%7D+%2B+b_%7B2%7D%5E%7Bnew%7D%7D%7B2%7D)



### 高斯核函数（RBF）

参考：[机器学习：SVM（核函数、高斯核函数RBF） - 何永灿 - 博客园 (cnblogs.com)](https://www.cnblogs.com/volcao/p/9465214.html)

#### 思想

- **业务的目的是样本分类，采用的方法：按一定规律统一改变样本的特征数据得到新的样本，新的样本按新的特征数据能更好的分类，由于新的样本的特征数据与原始样本的特征数据呈一定规律的对应关系，因此根据新的样本的分布及分类情况，得出原始样本的分类情况。**

1. 应该是试验反馈，将样本的特征数据按一定规律统一改变后，同类样本更好的凝聚在了一起；

- 高斯核和多项式核干的事情截然不同的，如果对于样本数量少，特征多的数据集，高斯核相当于对样本降维；

- **高斯核的任务**：找到更有利分类任务的新的空间。
- **方法**：类似 ![img](https://images2018.cnblogs.com/blog/1355387/201808/1355387-20180813091841921-939555460.png) 的映射。

 

- **高斯核本质是在衡量样本和样本之间的“相似度”，在一个刻画“相似度”的空间中，让同类样本更好的聚在一起，进而线性可分。**

- **疑问**：
- “衡量”的手段 ![img](https://images2018.cnblogs.com/blog/1355387/201808/1355387-20180813091841921-939555460.png)，经过这种映射之后，为什么同类样本能更好的分布在一起？

 

#### 定义方式

- ![img](https://images2018.cnblogs.com/blog/1355387/201808/1355387-20180813081806925-1258954945.png)；

1. $x、y$：样本或向量；
2. $γ$：超参数；高斯核函数唯一的超参数；
3. $|| x - y ||$：表示向量的范数，可以理解为向量的模；
4. 表示两个向量之间的关系，结果为一个具体值；
5. 高斯核函数的定义公式就是进行点乘的计算公式；

 

#### **功能**

- 先将原始的数据点$（x， y）$映射为新的样本$（x'，y'）$；
- 再将新的特征向量点乘，返回其点乘结果；



#### 特点

- **高斯核运行开销耗时较大，训练时间较长**；
- **一般使用场景**：数据集 (m, n)，m < n；
- **一般应用领域**：自然语言处理；

 

## **任务一：分别用线性SVM和高斯核SVM预测对数据进行分类**

### （1）问题描述：

task1_linear.mat中有一批数据点，试用线性SVM对他们进行分类，并在图中画分出决策边界。task1_gaussian中也有一批数据点，试用高斯核SVM对他们进行分类，并在图中画出决策边界。

### （2）训练过程：

#### **使用线性核函数的svm算法**

1. 加载数据并可视化：

   加载一个2维数据集：

   ```python
   X,y = svmF.loadData('task1_linear.mat')
   svmF.plotData(X,y)
   ```

   观察可知该数据集可以被线性边界分割为正样本和负样本。

   <img src="C:\Users\YuetianW\AppData\Roaming\Typora\typora-user-images\image-20210505170624080.png" alt="image-20210505170624080"  />

   

2. 训练模型与边界可视化：

   ```python
   model = svmF.svmTrain_SMO(X, y, C=1, max_iter=20)
   svmF.visualizeBoundaryLinear(X, y, model)
   ```

   变量 $C$所起的作用于逻辑回归中的正则化参数$\frac{1}{λ}$

   变量$C$值对决策边界有不同的影响，下面我们尝试分几种情况验证：

   - $C=1：$

     ![](https://files.catbox.moe/pvl45i.png)

   - $C=100:$

     ![](https://files.catbox.moe/7tr1pj.png)

   - $C=1000:$

     ![](https://files.catbox.moe/pf7d4y.png)

   

   我们可以发现，$C$的大小影响着线性决策边界，其所起的作用于逻辑回归中正则化参数一样，$C$太大，可能会导致过拟合问题。



#### 使用高斯核函数的SVM算法

对于非线性的分类任务，常用带有高斯核函数的SVM算法来实现。

1. 加载数据并可视化：

   加载一个2维数据集：

   ```python
   X, y = svmF.loadData('task1_gaussian.mat')
   svmF.plotData(X, y)
   ```

   可以很明显地看出是非线性的数据。

![image-20210505191056290](https://i.loli.net/2021/05/05/ITed9WswnbLmDNK.png)



2. 训练模型与边界可视化：

   ```python
   model = svmF.svmTrain_SMO(X, y, C=1, kernelFunction='gaussian', K_matrix=svmF.gaussianKernel(X, sigma=0.1))
   svmF.visualizeBoundaryGaussian(X, y, model,sigma=0.1)
   ```

   实现效果如下所示：

   ![image-20210505191920218](https://i.loli.net/2021/05/05/H4E2c8tAiFKY6Jm.png)



### （3）尝试调用sklearn：

- 调用sklearn svm，如下所示：

  ```python
  from sklearn import svm
  c = 1
  clf = svm.SVC(c, kernel='linear', tol=1e-3)
  clf.fit(X, y)
  
  
  ```

- 结果：

  ![image-20210505201011540](https://i.loli.net/2021/05/05/kdDzCB5Q9tU7r8v.png)

- 高斯核：

  ```python
  c = 1
  sigma = 0.1
  clf = svm.SVC(c, kernel='rbf', gamma=np.power(sigma, -2))
  clf.fit(X, y)
  ```

  

- 结果

  ![image-20210505201502681](https://i.loli.net/2021/05/05/pv1etqmwJrgQVF6.png)






## **任务二：使用高斯核SVM对给定数据集进行分类**

### （1）问题描述：

给定数据集（文件task2.mat）, 参考task1的代码, 编程实现一个高斯核SVM进行分类。输出训练参数C, sigma分别取0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30时(共64组参数组合)的训练集上的准确率。（程序运行时间8mins左右，准确率 = 预测正确样本数/样本总数 ）



### （2）实现过程：

1. 读入数据集并可视化数据：

   ```python
   X, y = svmF.loadData('task1_linear.mat')
   svmF.plotData(X, y)
   ```

   数据如下图示：

   ![image-20210506145103041](https://i.loli.net/2021/05/06/GohUkz6aKcyDd7B.png)

   

2. 寻找最优参数：

   寻找最优的参数c和sigma,题目中给定了8个c和sigma的值,两两之间组合一共是64种情况,然后从64种情况中,选择验证误差最小的参数组合。

   ```python
   def Find_Best_Param(X, y, Xval, yval):
       C_best = 0
       sigma_best = 0
       Clist = [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30]
       slist = [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30]
       predict_best = 0.0
       dlist = pd.DataFrame(columns=Clist, index=slist)
       dlist.index.name = 'sigma'
       dlist.columns.name = 'C'
       for C_now in Clist:
           for sigma_now in slist:
               classifier = svm.SVC(C=C_now, kernel='rbf', gamma=np.power(sigma_now, -2.0) / 2, decision_function_shape='ovr')
               classifier.fit(X, y)
               predict = classifier.score(Xval, yval)  # Returns the mean accuracy on the given test data and labels
               dlist.loc[sigma_now, C_now] = predict
               if predict > predict_best:
                   predict_best, C_best, sigma_best = predict, C_now, sigma_now
       print("Accuracy List:")
       print(dlist)
       return C_best, sigma_best, predict_best
   ```

   输出结果：

   ![image-20210506153658920](https://i.loli.net/2021/05/06/DEp9CJuFhGLgd3Q.png)

   

3. 最终模型：

   最后再将参数带入至模型中,画出模型对应的曲线。

   ```python
   model = svmF.svmTrain_SMO(X, y, C=1, kernelFunction='gaussian', K_matrix=svmF.gaussianKernel(X, sigma=0.1))
   svmF.visualizeBoundaryGaussian(X, y, model,sigma=0.1)
   ```

   画出边界如下图所示：

   ![image-20210506154434191](https://i.loli.net/2021/05/06/bzRq4dFTSDPEKcU.png)



## **任务三：使用线性SVM实现对垃圾邮件分类**

### （1）问题描述：

​    编程实现一个垃圾邮件SVM线性分类器，分别在训练集和测试集上计算准确率。其中训练数据文件：task3_train.mat，要求导入数据时输出样本数和特征维度。测试数据文件：task3_test.mat，要求导入数据时输出样本数和特征维度，测试数据标签未给出。（程序运行时间10mins左右）

### （2）实现过程：

1. 分析数据：

   利用给出loadData()，读取数据，并输出维度：

   ```python
   X, y = svmF.loadData('task3_train.mat')
   shape = np.shape(X)
   print('训练集样本数:%d,特征维度:%d' % (shape[0], shape[1]))
   
   '''
   output:
   训练集样本数:4000,特征维度:1899
   '''
   
   ```

   观察输入如下图所示：

   ![image-20210505210255981](https://i.loli.net/2021/05/05/GgYUXeWhTKltIas.png)

   可知，这里是已经完成了邮件特征变量的提取的数据。

   完成了邮件特征变量的提取之后, 可以利用4000个训练样本和1000个测试样本训练SVM算法, 每个原始的邮件将会被转化为一个 $x \in R^{1900}$ 的向量 (词汇表中有1899个词汇， $x_{0}=1$ 会 被添加到向量中）。

   

2. 训练模型：

   载入数据集之后, 用变量 $y=1$ 表示 垃圾邮件, 而 $y=0$ 表示非垃圾邮件可就可以训练SVM算法了。

   这里我们使用sklearn的svm，具体实现代码如下所示:

   ```python
   c = 0.1
   clf = svm.SVC(c, kernel='linear')
   clf.fit(X, y)
   ```

   在训练集上的精度如下：

   ```python
   p = clf.predict(X)
   print('Training Accuracy: {}'.format(np.mean(p == y) * 100))
   ```

   ![image-20210505220013881](https://i.loli.net/2021/05/05/Do43UMjGPJh5nB6.png)

   尝试高斯核：

   ```python
   c = 1
   sigma = 0.1
   clf = svm.SVC(c, kernel='rbf', gamma=np.power(sigma, -2))
   clf.fit(X, y)
   ```
   
   ![image-20210505220225375](https://i.loli.net/2021/05/05/rLKNs7cWQHyO1fh.png)



3. 输出预测结果：

   ```python
   result = clf.predict(X_t)
   np.savetxt('result.txt', result, fmt='%d', delimiter='\n')
   ```



## 实验小结：

- 支持向量机的参数选择
  $C:$对于C，C越大，可以理解为正则化系数越小，会出现lower bias和high variance的问题就是过拟合；C越小，可以理解为lambda越大，会出现high bias和low variance的问题就是欠拟合。

  sigma：对于高斯函数的sigma，sigma越大，特征变化越平滑，会出现high bias和low variance的问题就是欠拟合；sigma越小，特征变化越陡峭，会出现lower bias和high variance的问题就是过拟合。

- 核函数选择：

  当特征数量相对于训练集数量很大时，使用逻辑回归或者是使用线性核函数的支持向量机；
  当特征数量很少，训练集数据量一般，使用高斯核函数的支持向量机；
  当特征数量很少，训练集数据很大，可以考虑添加更多特征，然后使用逻辑回归或者是使用线性核函数的支持向量机。