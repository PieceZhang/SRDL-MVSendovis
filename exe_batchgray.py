# https://blog.csdn.net/qq_56839117/article/details/125216637
import cv2
import os

img_list = []
output_name = 'cam1'
input_path = r"D:\B_SRDL\SRDL-MVSendovis\imgcap\{}".format(output_name)  # 要处理的图片所在的文件夹
output_path = r"D:\B_SRDL\SRDL-MVSendovis\imgcap\{}_gray".format(output_name)  # 处理完的图片放在这里
for item in os.listdir(input_path):
    img_list.append(os.path.join(input_path, item))
print(list)
count = 0
for imagepath in img_list:
    # print(imagepath)
    image = cv2.imread(imagepath, cv2.IMREAD_GRAYSCALE)
    print(output_path + '\\' + '{}_{}.jpg'.format(count, output_name))  # 显示保存文件的路径及保存的文件名
    cv2.imwrite(output_path + '\\' + '{}_{}.jpg'.format(count, output_name), image)
    # 按一定路径将图片保存下来并命名，加号左边代表保存路径，右边代表文件命
    # %d代表后面的% count中的count的数值
    print("-----------执行中，保存第{}张----------".format(count + 1))
    count += 1
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imshow('garyimg', image)
    cv2.waitKey(0)
