# -*- coding: utf-8 -*-
"""
@File    : test.py
@Time    : 2020/5/26 18:09
@Author  : Dontla
@Email   : sxana@qq.com
@Software: PyCharm
"""
from matplotlib import pyplot as plt  # 用来绘制图形
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

X = 850
Y = 600
Z = 82.1


class Curve(object):
    def __init__(self, maxl=100):
        self.maxl = maxl
        self.data = np.ndarray([maxl])
        self.count = 0
        self.ifover = False

    def append(self, newdata):
        self.data[self.count] = newdata
        self.count += 1
        if self.count >= self.maxl:
            self.count = 0
            self.ifover = True

    def readline(self):
        if self.ifover:
            return np.concatenate([self.data[self.count:], self.data[:self.count]])
        else:
            return self.data[:self.count]

    def readpoint(self):
        print(self.count)
        return self.data[self.count - 1]


# 创建绘制实时损失的动态窗口
xcurve = Curve()
ycurve = Curve()
zcurve = Curve()

plt.ion()
for i in range(300):
    xcurve.append(X)
    ycurve.append(Y)
    zcurve.append(Z)
    plt.ion()
    plt.clf()  # 清除之前画的图
    fig = plt.gcf()  # 获取当前图
    ax = fig.gca(projection='3d')  # 获取当前轴
    ax.scatter3D(X, Y, Z)
    ax.plot(xcurve.read(), ycurve.read(), zcurve.read(), c='b')
    plt.pause(0.1)
    plt.ioff()

    Z = Z + i * 0.5  # 变换Z值

# 加这个的目的是绘制完后不让窗口关闭
plt.show()
