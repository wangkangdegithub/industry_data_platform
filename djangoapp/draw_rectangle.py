# -*- coding: utf-8 -*-
# file: draw_rectangle.py
# author: Wang Kang
# time: 01/11/2018 20:47 PM
# ----------------------------------------------------------------
import cv2
import numpy as np


def draw_rectangle(image):
    """
    画出EL边缘轮廓及格栅，减少不相关特征对故障特征的干扰
    :param image: 输入为 调整亮度/对比度后的图片（adjust_image_info（））
    :return:添加（白色）边缘的图片
    """
    imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 10, 255, cv2.THRESH_BINARY)

    # 反色，即对二值图每个像素取反
    result = cv2.bitwise_not(thresh)
    dilation_kernel = np.ones((10, 10), np.uint8)
    dilation = cv2.dilate(result, dilation_kernel, iterations=2)
    erode_kernel = np.ones((5, 5), np.uint8)
    closing_image = cv2.erode(dilation, erode_kernel, iterations=1)
    new_image, new_contours, new_hierarchy = cv2.findContours(closing_image, cv2.RETR_TREE,
                                                              cv2.CHAIN_APPROX_SIMPLE)  # image2的二值图经过形态学转化后的轮廓等
    for i in range(len(new_contours)):
        j = new_contours[i]
        x, y, w, h = cv2.boundingRect(j)
        cv2.rectangle(image, (x - 10, y - 10), (x + w + 8, y + h + 5), (255, 255, 255),17)  # 不注释的话会使之后的img变量表示的图片上都是绿色的线框存在，影响图片原有信息。

    # 保存到本地注释掉，在batch_deal_el.py中保存到本地，便于批处理
    # cv2.imwrite('D://Documents//Desktop//add_rectangle_image.jpg', ee)
    return image


if __name__ == '__main__':
    from tools import image_show
    image = cv2.imread('F:/2017/12/ELTD/Constract/Constract_101910111517.jpg')
    add_rectangle_image = draw_rectangle(image)
    image_show('add_rectangle_image',add_rectangle_image)