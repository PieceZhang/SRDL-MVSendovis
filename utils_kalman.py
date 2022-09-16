import numpy as np


class KalmanFilter:
    def __init__(self, Q=1, R=5):
        self.Q = Q
        self.R = R
        self.p_last = 10
        self.x_last = 0

    def predict(self, Z):
        a = 1
        b = 0
        c = 1

        # q = 0
        # r = 0
        # beta = 0.001
        # alpha = 50

        # 预测步
        x_ = a * self.x_last  # 预测当前状态
        p_ = a * self.p_last * a + self.Q
        e = Z - x_  # 计算残差

        # 更新步
        k = p_ * c / (c * p_ * c + self.R)
        x = x_ + k * e
        p = (1 - k * c) * p_

        self.p_last = p
        self.x_last = x

        return x
