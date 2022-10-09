import numpy as np
import cv2


def _get_polar_line(img: np.array, r, theta):
    size = img.shape
    center = [size[1] // 2, size[0] // 2]  # (x,y)
    theta_rad = theta * np.pi / 180
    w = int(r * np.cos(theta_rad))
    h = int(r * np.sin(theta_rad))
    if abs(w) >= abs(h):
        if h != 0:
            h_seq = np.arange(0, h, np.sign(h) * abs(h / w)).astype(np.int16)
        else:  # h==0
            h_seq = np.zeros((abs(w)), dtype=np.int16)
        if w > 0:
            w_seq = np.array(range(w), dtype=np.int16)
        else:  # w<0, w这里不可能等于0
            w_seq = np.array(range(1, w + 1, -1), dtype=np.int16)
    else:
        if w != 0:
            w_seq = np.arange(0, w, np.sign(w) * abs(w / h)).astype(np.int16)  # w - np.sign(w) -
        else:  # w==0
            w_seq = np.zeros((abs(h)), dtype=np.int16)
        if h > 0:
            h_seq = np.array(range(h), dtype=np.int16)
        else:  # h<0, h这里不可能等于0
            h_seq = np.array(range(1, h + 1, -1), dtype=np.int16)
    w_seq += center[0]
    h_seq += center[1]
    # seq = np.array([[_w, _h] for _w, _h in zip(w_seq, h_seq)])
    line = img[[h_seq], [w_seq]].squeeze()
    return line


def find_tip(img, box):
    center = [box[0] + box[2] // 2, box[1] + box[3] // 2]  # 圆心
    innerR = min(20, min(box[2], box[3]))  # 内圆半径
    outerR = innerR + 150  # 外圆半径
    anglegap = 30  # 搜索角度间隔 （度°）
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转换为灰度
    img = np.pad(img, outerR, constant_values=255)  # 用白色填充边缘
    center[0] += outerR
    center[1] += outerR
    outerimg = img[center[1] - outerR:center[1] + outerR, center[0] - outerR:center[0] + outerR]  # 按照外圆裁剪图片 (正方形近似)
    innerimg = img[center[1] - innerR:center[1] + innerR, center[0] - innerR:center[0] + innerR]  # 按照内圆裁剪图片 (正方形近似)
    img_center_avg = np.mean(innerimg)  # 计算中心像素平均值

    anglelist = np.array(range(0, 360, anglegap))
    linelist = np.zeros((len(anglelist)))
    vectorlist = np.ndarray((len(anglelist), 2))
    for index, angle in enumerate(anglelist):
        line = _get_polar_line(outerimg, outerR, angle)
        line = line[innerR:]  # 截去内圆
        line = np.sum(np.where(line > 2 * img_center_avg, -1, 1))  # 白色-1，黑色+1
        linelist[index] = line
        if 0 <= angle < 90:
            vectorlist[index, 0] = line * np.cos(angle)
            vectorlist[index, 1] = line * np.sin(angle)
        if 90 <= angle < 180:
            vectorlist[index, 0] = line * np.cos(angle - 90)
            vectorlist[index, 1] = line * np.sin(angle - 90)
            vectorlist[index, 0] *= -1
        elif 180 <= angle < 270:
            vectorlist[index, 0] = line * np.cos(angle - 180)
            vectorlist[index, 1] = line * np.sin(angle - 180)
            vectorlist[index, 0] *= -1
            vectorlist[index, 1] *= -1
        elif 270 <= angle < 360:
            vectorlist[index, 0] = line * np.cos(angle - 270)
            vectorlist[index, 1] = line * np.sin(angle - 270)
            vectorlist[index, 1] *= -1
    x = np.sum(vectorlist[:, 0])
    y = np.sum(vectorlist[:, 1])
    radius = np.sqrt(x * x + y * y)
    theta = np.arcsin(y / radius) * 180 / np.pi
    print(theta, radius)


if __name__ == '__main__':
    bbox = np.load('./sample/bbox.npz')
    bbox1 = bbox['bbox1']
    bbox2 = bbox['bbox2']
    del bbox

    camera1_frame = cv2.imread('./sample/test1.png')
    camera2_frame = cv2.imread('./sample/test2.png')
    # cv2.rectangle(camera1_frame, (bbox1[0], bbox1[1]),
    #               (bbox1[0] + bbox1[2], bbox1[1] + bbox1[3]),
    #               (0, 255, 0), 3)
    # cv2.rectangle(camera2_frame, (bbox2[0], bbox2[1]),
    #               (bbox2[0] + bbox2[2], bbox2[1] + bbox2[3]),
    #               (0, 255, 0), 3)
    # cv2.circle(camera1_frame, (bbox1[0] + bbox1[2] // 2, bbox1[1] + bbox1[3] // 2), 3, (0, 255, 0), 2)
    # cv2.circle(camera2_frame, (bbox2[0] + bbox2[2] // 2, bbox2[1] + bbox2[3] // 2), 3, (0, 255, 0), 2)

    cv2.namedWindow("test")
    # cv2.imshow("test", camera1_frame)
    # cv2.waitKey(0)
    # cv2.imshow("test", camera2_frame)
    # cv2.waitKey(0)

    testframe = np.ones((500, 500, 3), dtype=np.uint8) * 255
    testbox = [240, 240, 20, 20]
    cv2.circle(testframe, (250, 250), 20, (0, 0, 0), 40)
    find_tip(testframe, testbox)

    for bbox, frame in zip([bbox1, bbox2], [camera1_frame, camera2_frame]):
        finalbbox = find_tip(frame, bbox)
