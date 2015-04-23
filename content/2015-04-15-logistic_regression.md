title: 机器学习笔记——逻辑回归(LogisticRegression)
date:2015-04-15 16:05:55
Tags:机器学习,Codes
comments: true 
Category:Study

### 基本概念
逻辑回归是一种线性分类的方法，通过给定一些样本空间中的样本点，训练出一条直线（超平面)，使得样本点能被较好的分隔开。
设$\theta=[\theta_1 \theta_2 \cdots \theta_n]^T$为分类面参数，$x=[x_1 x_2 \cdots x_n]^T$，则有：
$$
h_\theta(x)=
\begin{cases}
1 ,& \theta^T \cdot x \ge 0 \\
0 ,& \theta^T \cdot x < 0
\end{cases}
$$
通过这样拟合直线的方式就可以得到一组参数，将样本分为两类。

引入S函数(也称作Logistic函数)：
$$sigmoid(x)=\frac{1}{1+e^{-x}}$$
函数图像如下图所示，它可以将自变量映射在(0,1)的区间内，则把0/1分类的结果转化为样本点属于某个类的概率。

![sigmoid函数](sigmoid.png)

这样可以写成
$$ h_\theta(x)=sigmoid(\theta^T \cdot x)$$。
设概率 $$P(y=1|x;\theta)=h_\theta(x)$$,即在给定的参数$\theta$下，样本x被分到1类的概率。则样本被分到0类的概率为：
$$P(y=0|x;\theta)=1-h_\theta(x)$$
考虑到y的取值只有0和1，则可以得到概率密度如下：
$$
p(y|x;\theta)=h_\theta(x)^y(1-h_\theta(x))^{1-y}
$$
设所有样本都是独立的，则可以得到联合概率分布：
$$p(\vec y | X;\theta)=\prod_{i=1}^m p(y^{(i)}|x^{(i)};\theta)=\prod_{i=1}^mh_\theta(x^{(i)})^{y^{(i)}}(1-h_\theta(x^{(i)}))^{1-y^{(i)}}$$

用极大似然估计的想法来进行参数$\theta$的估计，则使得上式达到最大值的$\theta$就是最终求解的目标。在这里，我们使用梯度下降的方法来求这个最大值。取对数似然概率,并对$\theta_j$求导可得：
$$ L=ln(p(\vec y | X;\theta))=\sum_{i=1}^m \{( y^{(i)}ln(h_\theta(x^{(i)})) + (1-y^{(i)}ln((1-h_\theta(x^{(i)}))\}$$

$$ \frac{\partial L}{\partial \theta_j} = \sum_{i=1}^m\{\frac{y^{(i)}}{h_\theta(x^{(i)})}\cdot h_\theta^,(x^{(i)}) -
\frac{1-y^{(i)}}{1-h_\theta(x^{(i)})}\cdot h_\theta^,(x^{(i)})\}
$$
由Sigmoid函数的特性可知道:
$$
\begin{aligned}
 sigmoid^,(x) &= (\frac{1}{1+e^{-x}})^, \\
              &= \frac{e^{-x}}{(1+e^{-x})^2}\\
              &= \frac{1}{1+e^{-x}}-\frac{1}{(1+e^{-x})^2}\\
              &= \frac{1}{1+e^{-x}}(1-\frac{1}{1+e^{-x}})\\
              &= sigmoid(x)\cdot (1-sigmoid(x))
\end{aligned}
$$
因此，该对数概率的导数可以化为：
$$ 
\begin{aligned}
\frac{\partial L}{\partial \theta_j} &= \sum_{i=1}^m\{\frac{y^{(i)}}{h_\theta(x^{(i)})} -
\frac{1-y^{(i)}}{1-h_\theta(x^{(i)})}\}\cdot h_\theta^,(x^{(i)}) \\
&=\sum_{i=1}^m\{\frac{y^{(i)}}{h_\theta(x^{(i)})} -
\frac{1-y^{(i)}}{1-h_\theta(x^{(i)})}\} \cdot h_\theta(x^{(i)})\cdot(1-h_\theta(x^{(i)}))\cdot x_j^{(i)}\\
&= \sum_{i=1}^m ( y^{(i)}\cdot(1-h_\theta(x^{(i)}) -
(1-y^{(i)})\cdot h_\theta(x^{(i)}) ) \cdot x_j^{(i)}\\
&=\sum_{i=1}^m (y^{(i)} -  h_\theta(x^{(i)}))\cdot x_j^{(i)}
\end{aligned}
$$

梯度方向是上升最快的方向，因此参数的更新就按照梯度方向更新，可以得到：
$$
\theta_j = \theta_j + \alpha \frac{\partial L}{\partial \theta_j} = \theta_j + \alpha \cdot \sum_{i=1}^m (y^{(i)} -  h_\theta(x^{(i)}))\cdot x_j^{(i)}
$$
其中，$\alpha$是学习速率，设的太小收敛速度会很慢，设的太大的话，容易出现震荡，导致不收敛，可以在试验中自己调节，一般设为$\alpha \in (0,1]$。考虑到初始的时候，需要一个较大的学习速率来逼近结果。而学习一段时间以后需要降低学习速率防止震荡。因此可以随着迭代次数动态的调整学习速率。一个简单而常用的办法是设$t$为迭代次数，则有： 
$$
\alpha = \frac{1}{\sqrt{t}}
$$

###一些改进
上面描述的梯度下降方法，每一次更新时考虑了全部样本的梯度。这样的方法在数据量很大的时候，会导致每一次更新的时间很长，总收敛时间长到无法忍受。因此有人提出了[随机梯度下降(SGD)](http://en.wikipedia.org/wiki/Stochastic_gradient_descent),它在每次更新时，只考虑当前样本，即更新方程变为：
$$
\theta_j =  \theta_j + \alpha \cdot (y^{(i)} -  h_\theta(x^{(i)}))\cdot x_j^{(i)}
$$
这样的更新方式比原先快了很多，代价是会引入一定的噪声。用这个方程进行更新，总的误差曲线并不是一直降低，而是类似随机跳动的方式，但是总体还是向着最优解的方向移动。而且在数据量很大的时候，只需要少量的样本就可以让参数更新的足够好了。因此这种方法得到了较多的应用。