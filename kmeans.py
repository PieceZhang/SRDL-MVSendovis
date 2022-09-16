# -*- coding:utf-8 -*-
# https://blog.csdn.net/qq_36810544/article/details/102687097
# =========================

import numpy as np
import cv2
from sklearn.cluster import KMeans
import math
import matplotlib.pyplot as plt
from PIL import Image
from pylab import *
from sklearn import metrics


def color_cluster(img_file, k=2):
    """
    计算输入图像在HSV空间的聚类结果
    :param img_file: 图片文件路径
    :param k: 类别数
    :return: 返回聚类结果，标签值， 每个值的总数， 标签对应的rgb值, 本次聚类的得分， 像素的标签矩阵。numpy的array格式
    """
    img = img_file
    data = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    data = data.reshape((-1, 3))
    kmeans = KMeans(n_clusters=k, n_init=1, max_iter=5).fit(data)
    pixel_label = kmeans.labels_

    # 计算聚类得分，Calinski-Harabasz分数值越大聚类结果越好
    # ch_score = metrics.calinski_harabaz_score(data, pixel_label)
    ch_score = 0

    label_value = set(list(pixel_label))
    label_count = []
    hsv_avg = []
    for value in label_value:
        label_count.append(np.sum(pixel_label == value))
        hsv_mean = (np.sum(data[pixel_label == value], axis=0) / np.sum(pixel_label == value)).astype(np.uint8)
        hsv_avg.append(hsv_mean)
    hsv_array = np.reshape(np.array(hsv_avg), (k, 1, 3))
    rgb_array = cv2.cvtColor(hsv_array, cv2.COLOR_HSV2RGB)
    rgb_array = np.reshape(rgb_array, (k, 3))
    return np.array(list(label_value)), np.array(label_count), rgb_array, ch_score, pixel_label


# def show(label_value, label_count, rgb_array, k, raw_img, render_img):
#     # 可视化显示
#     # 设置默认字体，否则中文乱码
#     mpl.rcParams['font.family'] = "SimHei"
#     plt.subplot(221)
#     plt.title(u'原图')
#     plt.imshow(raw_img)
#
#     plt.subplot(222)
#     plt.title(u'主色统计')
#     plt.bar(label_value, label_count, 0.5, alpha=0.4, color='g', label='Num')
#
#     plt.subplot(223)
#     plt.title(u'主色排序')
#     color_img = np.zeros((400, k * 200, 3), dtype=np.uint8)
#     for i in range(k):
#         color_img[:, i * 200: (i + 1) * 200] = rgb_array[i]
#     color_img = Image.fromarray(color_img)
#     plt.imshow(color_img)
#
#     plt.subplot(224)
#     plt.imshow(render_img)
#     plt.show()
#
#
# def show2(raw_img, renders, start_k):
#     mpl.rcParams['font.family'] = "SimHei"
#     total_imgs = len(renders) + 1
#     # 向上取整
#     n_row = math.ceil(total_imgs / 4)
#     plt.subplot(n_row, 4, 1)
#     plt.title(u'原图')
#     plt.imshow(raw_img)
#     for index, render_img in enumerate(renders):
#         plt.subplot(n_row, 4, index + start_k)
#         plt.title('k = {0}'.format(index + start_k))
#         plt.imshow(render_img)
#     plt.show()


def render(img_size, pixel_label, label_value, rgb_array):
    img_shape = (img_size[1], img_size[0], 3)
    img = np.zeros(img_shape, dtype=np.uint8)
    pixel_label = np.reshape(pixel_label, (img_size[1], img_size[0]))
    for i, value in enumerate(label_value):
        img[pixel_label == value] = rgb_array[i]
    # render_img = Image.fromarray(img)
    return img


if __name__ == '__main__':
    img_file = r'./test.jpg'
    raw_img = Image.open(img_file)

    label_value, label_count, rgb_array, score, pixel_label = color_cluster(cv2.imread(img_file))
    render_img = render(raw_img.size, pixel_label, label_value, rgb_array)
    # show(label_value, label_count, rgb_array, k, raw_img, render_img)
    # show2(raw_img, renders, 2)
    plt.subplot(1, 2, 1), plt.imshow(raw_img)
    plt.subplot(1, 2, 2), plt.imshow(Image.fromarray(render_img))
    plt.show()



    # capture = cv2.VideoCapture(0)
    # while True:
    #     ret, frame = capture.read()
    #     frame = cv2.flip(frame, 1)  # 镜像操作
    #
    #     label_value, label_count, rgb_array, score, pixel_label = color_cluster(frame)
    #     render_img = render(frame.shape, pixel_label, label_value, rgb_array)
    #
    #     cv2.imshow("frame", frame)
    #     cv2.imshow("render_img", render_img)
    #     key = cv2.waitKey(5)
    #     if key == ord('q'):
    #         break
    #
    # cv2.destroyAllWindows()
