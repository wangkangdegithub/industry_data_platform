# -*- coding: utf-8 -*-
# file: 轮廓提取.py
# author: Wang Kang
# time: 01/11/2018 20:47 PM
# 边缘轮廓、格栅提取。参数设定以调整过对比度的Constract目录下图片为准。编著图片：'D://Documents//Desktop//sxdhd.jpg'
# ----------------------------------------------------------------

import numpy as np
import cv2

path_file = "F:/2017/12/ELTD/Constract/Constract_1019101127101.jpg"
img = cv2.imread(path_file)
imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

cv2.namedWindow('imgray', cv2.WINDOW_NORMAL)
cv2.imshow('imgray',imgray)
cv2.waitKey(0)
cv2.destroyAllWindows()

ret,thresh = cv2.threshold(imgray,10,255, cv2.THRESH_BINARY);
#反色，即对二值图每个像素取反
result = cv2.bitwise_not(thresh);
#显示图像
cv2.namedWindow('result', cv2.WINDOW_NORMAL)
cv2.imshow("result",result)
cv2.waitKey(0)
cv2.destroyAllWindows()

dilation_kernel = np.ones((10, 10), np.uint8)
dilation = cv2.dilate(result, dilation_kernel, iterations=2)
erode_kernel = np.ones((5, 5), np.uint8)
closing_image = cv2.erode(dilation, erode_kernel, iterations=1)

cv2.namedWindow('closing_image', cv2.WINDOW_NORMAL)
cv2.imshow("closing_image",closing_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

new_image, new_contours, new_hierarchy = cv2.findContours(closing_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)   # image2的二值图经过形态学转化后的轮廓等

for i in range(len(new_contours)):
    j = new_contours[i]
    x, y, w, h = cv2.boundingRect(j)
    cv2.rectangle(img, (x-10, y-10), (x + w+5 , y + h+5 ), (255, 255, 255),14)  # 不注释的话会使之后的img变量表示的图片上都是绿色的线框存在，影响图片原有信息。

cv2.namedWindow('image', cv2.WINDOW_NORMAL)  # 在一张图片里显示出所有边缘矩形
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()


