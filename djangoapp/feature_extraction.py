# -*- coding: utf-8 -*-
# file: feature_extraction.py
# author: Wang Kang
# time: 12/26/2017 17:23 PM
# ----------------------------------------------------------------
import cv2
import numpy as np
from djangoapp import models

def Contours_feature(picture):
    """
    输入图片的轮廓特征等信息.
    :param picture: 输入.
    :return: thresh,image,contours,分别为转化后的二值图、转化后的二值图、轮廓.
    """
    imgray = cv2.cvtColor(picture,cv2.COLOR_BGR2GRAY)
    #  cv2.threshold() 的第二个值的设置很重要
    ret,thresh = cv2.threshold(imgray,60,255, cv2.THRESH_BINARY_INV)   # 第一个参数就是原图像，原图像应该是灰度图。第二个参数就是用来对像素值进行分类的阈值。第三个参数就是当像素值高于（有时是小于）阈值时应该被赋予的新的像素值。
    image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    return thresh,image,contours


def transform_form(thresh,transform_type):
    """
    二值图形态学转换，以便特征的提取.
    :param thresh: 二值图输入.
    :param transform_type: 形态转换类型.
    :return: thresh,image,contours,分别为转化后的二值图、输入图片、轮廓.
    """
    if transform_type == 'closing':       # 闭运算：先膨胀再腐蚀
        dilation_kernel = np.ones((5, 5), np.uint8)
        dilation = cv2.dilate(thresh, dilation_kernel, iterations=1)
        erode_kernel = np.ones((5, 5), np.uint8)
        closing_image = cv2.erode(dilation, erode_kernel, iterations=2)         # 腐蚀 增加黑色区域
        return closing_image
    elif transform_type == 'opening':        # 开运算：先腐蚀再膨胀
        kernel = np.ones((10, 10), np.uint8)
        opening_image = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)        # 先进性腐蚀再进行膨胀就叫做开运算。就像我们上面介绍的那样，它被用来去除噪声。
        return opening_image


def bounding_show(two_valued_contours,original_need_deal_el_path,number_id):
    """
    在原图中画出矩形框且包含轮廓
    :param two_valued_contours: 二值化后的轮廓列表.
    :param original_need_deal_el_path: 输入未作对比度亮度处理的EL的路径.
    :param num: 批处理时处理EL图片张数的计数.
    :return: thresh,image,contours,分别为转化后的二值图、输入图片、轮廓.
    """
    bounding_list = []
    filename = number_id
    # EL单一特征全图绘制并写到指定目录下
    for i in range(len(two_valued_contours)):
        j = two_valued_contours[i]

        # 不清楚什么原因：在想要输出单一特征全图时，初始化中间变量middle_adjust_light_contrast_img为EL调整后对比度的图片，
        # 如果直接为其赋值变量adjust_light_contrast_img时，实际上每次循环后并没有重新复制对应的数据。所以为变量赋上路径
        # middle_adjust_light_contrast_img = cv2.imread('D://Documents//Desktop//over_picture.jpg')
        x,y,w,h = cv2.boundingRect(j)
        area = cv2.contourArea(j)
        if  w < 900 and area>50:
            bounding_list.append((x,y,w,h))
        else :
            continue

    bounding_list = sorted(bounding_list, key=lambda x: x[0])  # 对提取的边缘 面积从小到大排序
    for m in range(len(bounding_list)):  # 对每个边缘求出图像
        global original_need_deal_el_img
        feature_bounding_box = bounding_list[m]
        m += 1
        x, y, w, h = feature_bounding_box
        original_need_deal_el_img = cv2.imread(original_need_deal_el_path)
        cv2.rectangle(original_need_deal_el_img, (x - 10, y - 10), (x + w + 10, y + h + 10), (0, 255, 0),2)     # 不注释的话会使之后的img变量表示的图片上都是绿色的线框存在，影响图片原有信息。
        cv2.imwrite('F://untitled//media//%s_%s_%s.jpg' % (filename, 1, m),original_need_deal_el_img)           # EL单一特征全图写到本地指定文件夹


    # EL特征全图绘制
    for k in two_valued_contours:
        x,y,w,h = cv2.boundingRect(k)
        area = cv2.contourArea(k)
        if  w < 900 and area>50:                                                      # x,y 后面+10 的目的是为了让矩形框面积变大，最大化包含轮廓信息
            cv2.rectangle(original_need_deal_el_img, (x-10, y-10),
                          (x + w + 10, y + h + 10), (0, 255, 0), 2)                   # 不注释的话会使之后的img变量表示的图片上都是绿色的线框存在，影响图片原有信息。
            bounding_list.append((x,y,w,h))
        else :
            continue
    cv2.imwrite('F://untitled//media//%s_%s.jpg' % (filename,1),original_need_deal_el_img)


def save_bounding_picture(two_valued_contours,original_need_deal_el_path,number_id,constract_el_path,rectangle_el_path):
    """
    保存轮廓图片到本地
    :param two_valued_contours: 二值化后的轮廓列表.
    :param original_need_deal_el_path: 输入为作对比度亮度处理的EL的路径。
    :param number_id: 批处理时处理EL图片的id.
    """
    bounding_list = []
    original_need_deal_el_img = cv2.imread(original_need_deal_el_path)
    filename = number_id
    for i in two_valued_contours:
        x, y, w, h = cv2.boundingRect(i)
        area = cv2.contourArea(i)
        if w < 900 and area > 50:
            bounding_list.append((x, y, w, h))
        else:
            continue
    bounding_list = sorted(bounding_list, key=lambda x: x[0])  # 对提取的边缘 面积从小到大排序
    for j in range(len(bounding_list)):  # 对每个边缘求出图像
        feature_bounding_box = bounding_list[j]
        j += 1
        x, y, w, h = feature_bounding_box  # Grab the coordinates of the letter in the image
        feature_image = original_need_deal_el_img[y - 10:y + h + 10,x - 10:x + w + 10]          # Extract the letter from the original image with a 2-pixel margin around the edge
        cv2.imwrite('F://2017//12//ELTD//STZ//%s_%s_%s_s.jpg' % (filename,1,j),feature_image)   # 每个边缘矩形图像保存到本地
        dytz_el_path = 'F://2017//12//ELTD//STZ//%s_%s_%s_s.jpg' % (filename,1,j)
        # 字段1-6
        dytzqt_el_path = 'F://untitled//media//%s_%s_%s.jpg' % (filename, 1, j)
        tzqt_el_path = 'F://untitled//media//%s_%s.jpg' % (filename, 1)
        models.TestELimg.objects.create(original_el_path=original_need_deal_el_path,constract_el_path=constract_el_path,
                                        rectangle_el_path=rectangle_el_path,dytzqt_el_path = dytzqt_el_path,
                                        tzqt_el_path=tzqt_el_path,dytz_el_path=dytz_el_path)
    print('边缘矩形图像已保存到本地')



if __name__ == '__main__':
    from tools import image_show
    over_picture_path = 'D://Documents//Desktop//over_picture.jpg'
    #original_image = cv2.imread('D://Documents//Desktop//over_picture.jpg')    # 改变亮度、对比度后的图片image1
    image = cv2.imread('D://Documents//Desktop//add_rectangle_image.jpg')      # 在image1的基础上增加矩形边缘、白色格栅线的图片image2

    # 图片img的二值图和轮廓等。
    thresh = Contours_feature(image)[0]
    transformed_image = transform_form(thresh, 'closing')
    image_show('transformed_image',transformed_image)           # 展示形态学转换后的二值图
    new_image, new_contours, new_hierarchy = cv2.findContours(transformed_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)   # image2的二值图经过形态学转化后的轮廓等提取
    bounding_show(new_contours, over_picture_path)                 # 在image1 中展示故障特征
    save_bounding_picture(new_contours, over_picture_path)         # 根据轮廓，提取故障特征保存在本地