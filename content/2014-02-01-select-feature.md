title:选择适合跟踪的特征点
date:2014-02-01 21:47:04
comments: true 
Tags:计算机视觉
Category:Study

##问题
虽然现在已经得到了求解一个点的光流的方法，但是并不是什么点都能求出正确的光流。举一个例子就是，选择了一面白墙上的一个点，由于缺乏纹理信息，算法会失效。求解光流的方程如下：
$$
v=G^{-1}b
$$
其中：
\begin{equation}
\label{G}
G=\sum\sum\left[ \begin{array} {cc}
 I_xI_x &  I_xI_y \\\
 I_xI_y &  I_yI_y
\end{array}\right]
\end{equation}
$$
b=\sum\sum
\left[ \begin{array} {c}
\delta II_x\\\
\delta II_y 
\end{array}\right]
$$
从方程可以看出，当一个点周围的内容都一眼的话，$I_x$$I_y$都可能会很小，那么$det(G)$的值会很小，则不能求逆，导致求解不了。

所以做跟踪或者匹配的时候，总希望在物体中提取出一些适合跟踪的特征点，把这些适合跟踪的点输入给跟踪器。这就需要一个提取特征点的方法。好的特征点应该能够对旋转和平移运动不变，这样才能稳定的被跟踪。
## KLT特征点
KLT特征点是由LK方法的作者以及另一个叫Tomasi的人提出的。因为总会提到一个点及其邻域内的点这样的话，所以先定义**一个特征点**,为**一个点及其临域内的点**。

###简单的版本
简单一点的想法就是，因为解方程时需要求矩阵$\ref{G}$的逆，所以该矩阵需要是可逆的。二阶可逆矩阵会有两个非零特征值。只要最小特征值足够大，该矩阵就可逆，就能够求解光流。因此在求一个特征点的光流前，可以通过判断$\ref{G}$的最小特征值是否大于一个阈值，就可以知道算法是否会失效。

###复杂但是更有效的版本
既然算法失效的原因在于，特征点缺乏纹理信息，它包含的信息量太少。那么一个直观的想法就是，对于信息量少的特征点，就认为它是不好跟踪的点。对于包含信息量大的特征点，就认为它是好跟踪的点，把它保留下来。在主成分分析(PCA)中曾提到过，二维平面上的点集的协方差矩阵(2&times;2)表示了其中的各个点之间的关系，而该协方差矩阵的特征值就代表了这些点的分散程度，也就是所包含信息量的大小。在PCA中可以通过提取最大特征值的方法，把最主要的成分提取出来。而在这里，需要判断的是特征点所含信息量的大小，所以只要求出特征点协方差矩阵的最小特征值，只要这个次要成分也包含有足够量的信息，那么就可以认为该特征点是适合被跟踪的。

特征值的取值有如下几个情况：

1. $\lambda_1$ > $\lambda_2$ >>0 ，说明该特征点包含足够的信息
2. $\lambda_1$ >>0,$\lambda_2$ 接近0,说明该特征点只在一个方向包含信息，另一个方向没什么变化。例如边界点
3. $\lambda_1$，$\lambda_2$接近0, 没什么有用的信息，这个点不能要

综上，协方差矩阵的最小特征值越大，说明该特征点越适合被跟踪。

##求出最小特征值之后

为了找到适合跟踪的特征点，我们求解了每个点的协方差矩阵的特征值。找到最小特征值后，从大到小排序，去掉小于一个阈值的所有点(通常有了后续的操作，这一步可以省略）。对于这些特征点，只保留局部最大值。例如对于一个点，保留它的条件是：它的最小特征值是临域内最大的。那么邻域内其他点就需要去掉。 这样剩下的点都是比较适合的点了。但一般这样会剩下大量的点，而且非常密集，这会消耗很多计算，同时由于点太密集，全都求的话意义不大，所以设定一个最小距离，只保留那些互相之间距大于最小距离的点。

经过这些步骤，保留下来的点就都是适合跟踪的点了。