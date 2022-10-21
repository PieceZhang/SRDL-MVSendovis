# https://blog.csdn.net/qq_38784098/article/details/82144106
# CV模型：https://blog.csdn.net/weixin_40673873/article/details/106742431

import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
import time


def mat_math(intput, arg, im):
    output = intput
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            if arg == "atan":
                output[i, j] = math.atan(intput[i, j])
            if arg == "sqrt":
                output[i, j] = math.sqrt(intput[i, j])
    return output


def CV(LSF, im, mu, nu, epison, step):
    # Chan-Vese (CV) model
    Drc = (epison / math.pi) / (epison * epison + LSF * LSF)
    Hea = 0.5 * (1 + (2 / math.pi) * mat_math(LSF / epison, "atan", im))
    Iy, Ix = np.gradient(LSF)
    s = mat_math(Ix * Ix + Iy * Iy, "sqrt", im)
    Nx = Ix / (s + 0.000001)
    Ny = Iy / (s + 0.000001)
    Mxx, Nxx = np.gradient(Nx)
    Nyy, Myy = np.gradient(Ny)
    cur = Nxx + Nyy
    Length = nu * Drc * cur

    Lap = cv2.Laplacian(LSF, -1)
    Penalty = mu * (Lap - cur)

    s1 = Hea * im
    s2 = (1 - Hea) * im
    s3 = 1 - Hea
    C1 = s1.sum() / Hea.sum()
    C2 = s2.sum() / s3.sum()
    CVterm = Drc * (-1 * (im - C1) * (im - C1) + 1 * (im - C2) * (im - C2))

    LSF = LSF + step * (Length + Penalty + CVterm)
    # plt.imshow(s, cmap ='gray'),plt.show()
    return LSF


def LevelSet(im, rect):
    # 初始水平集函数
    IniLSF = np.ones((im.shape[0], im.shape[1]), im.dtype)
    IniLSF[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]] = -1
    IniLSF = -IniLSF
    # 模型参数
    mu = 1
    nu = 0.0005 * 255 * 255
    num = 5
    epison = 1
    step = 0.02
    LSF = IniLSF
    for i in range(1, num):
        t = time.time()
        LSF = CV(LSF, im, mu, nu, epison, step)  # 迭代
        t = time.time() - t

        plt.imshow(Image), plt.xticks([]), plt.yticks([])
        plt.contour(LSF, [0], colors='r')
        plt.draw(), plt.show(block=False), plt.pause(0.01)
        print(i, t)


if __name__ == '__main__':
    Image = cv2.imread('sample/test4_.jpg', 1)  # 读入原图
    # Image = cv2.resize(Image, (320, 180), interpolation=cv2.INTER_CUBIC)
    init_rect = cv2.selectROI("Image", Image, False, False)

    img = cv2.cvtColor(Image, cv2.COLOR_BGR2GRAY)
    img = np.array(img, dtype=np.float64)  # 读入到np的array中，并转化浮点类型

    Image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
    plt.figure(1), plt.imshow(Image), plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.draw(), plt.show(block=False)

    LevelSet(img, init_rect)

    cv2.waitKey(0)
