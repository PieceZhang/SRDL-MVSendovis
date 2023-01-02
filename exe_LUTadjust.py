import numpy as np
import cv2 as cv

if __name__ == '__main__':
    img = cv.imread("./sample/test5.jpg", flags=1)  # 读取彩色

    maxG = 128  # 修改颜色通道最大值，0<=maxG<=255
    lutHalf = np.array([int(i * maxG / 255) for i in range(256)]).astype("uint8")
    lutEqual = np.array([i for i in range(256)]).astype("uint8")

    lut3HalfB = np.dstack((lutHalf, lutEqual, lutEqual))  # (1,256,3), B_half/BGR
    lut3HalfG = np.dstack((lutEqual, lutHalf, lutEqual))  # (1,256,3), G_half/BGR
    lut3HalfR = np.dstack((lutEqual, lutEqual, lutHalf))  # (1,256,3), R_half/BGR

    blendHalfB = cv.LUT(img, lut3HalfB)  # B 通道衰减 50%
    blendHalfG = cv.LUT(img, lut3HalfG)  # G 通道衰减 50%
    blendHalfR = cv.LUT(img, lut3HalfR)  # R 通道衰减 50%

    cv.imshow('blendHalfB', blendHalfB)
    cv.imshow('blendHalfG', blendHalfG)
    cv.imshow('blendHalfR', blendHalfR)
    cv.waitKey(0)

