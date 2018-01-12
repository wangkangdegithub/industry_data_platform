# -*- coding: utf-8 -*-
# file: whole_step.py
# author: Wang Kang
# time: 01/09/2018 00:18 AM
# whole_step.py的批处理步骤
# ----------------------------------------------------------------
# 批处理多张图片。假设图片存放在'F://2017//12//ELTD//REnamepath'路径下面，则👇👇👇👇👇👇👇👇👇👇👇👇

"""
图片处理流程:
（原图）            10 月-19 日-18 时-59 分-47 秒-952 毫秒.jpg
 (原图重命名)       1019185947953.jpg                 ---->
（调整亮度对比度）	Constract_1019185947953.jpg   	 ---->
（画出边缘轮廓）		Rectangle_1019185947953.jpg  	 ---->
（EL特征全图）		1019185947953_1.jpg              ---->
（EL单一特征全图）	1019185947953_1_1.jpg
（EL单一特征全图）	1019185947953_1_2.jpg	   	     ---->
（EL单一特征）		1019185947953_1_1_s.jpg
（EL单一特征）		1019185947953_1_2_s.jpg
"""

import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "untitled.settings")# project_name 项目名称
django.setup()
from djangoapp.adjust_light_contrast import light_contrast_coef,adjust_image_info
from djangoapp.draw_rectangle import draw_rectangle
from djangoapp.feature_extraction import *
from djangoapp.cnn import *
from djangoapp.renamefile import *
from djangoapp import models


img = cv2.imread('D://Documents//Desktop//sxdhd.jpg')  # 标准图片
standard_light_coef = light_contrast_coef(img)[0]      # 标准图片
standard_contrast_coef = light_contrast_coef(img)[1]   # 标准图片
need_deal_path = 'F://2017//12//ELTD//REnamepath'

num = 0
for i in os.listdir(need_deal_path):
    num += 1
    number_id = i.split('.')[0]
    need_deal_el = os.path.join(need_deal_path,i).replace('\\','//')

    over_picture = adjust_image_info(need_deal_el, standard_light_coef, standard_contrast_coef)
    cv2.imwrite('F://2017//12//ELTD//Constract//Constract_%s.jpg' %number_id, over_picture)
    constract_el_path = 'F://2017//12//ELTD//Constract//Constract_%s.jpg' %number_id

    over_picture_test = cv2.imread('F://2017//12//ELTD//Constract//Constract_%s.jpg' %number_id)
    # 对over_picture画边缘白线，排除干扰项。处理后的图片保存到本地 'Rectangle_10100402220_1.jpg'
    add_rectangle_image = draw_rectangle(over_picture_test)
    cv2.imwrite('F://2017//12//ELTD//Rectangle//Rectangle_%s.jpg' %number_id, add_rectangle_image)
    rectangle_el_path = 'F://2017//12//ELTD//Rectangle//Rectangle_%s.jpg' %number_id

    # 为何直接调用变量add_rectangle_iamge 会报错？重新读路径正常？百思不得其解...
    image = cv2.imread('F://2017//12//ELTD//Rectangle//Rectangle_%s.jpg' %number_id )# 在image1的基础上增加矩形边缘、白色格栅线的图片image2
    thresh = Contours_feature(image)[0]
    transformed_image = transform_form(thresh, 'closing')
    #image_show('transformed_image', transformed_image)  # 展示形态学转换后的二值图
    new_image, new_contours, new_hierarchy = cv2.findContours(transformed_image, cv2.RETR_TREE,
                                                              cv2.CHAIN_APPROX_SIMPLE)  # image2的二值图经过形态学转化后的轮廓等提取

    # 为何直接调用变量over_picture 会报错？重新读路径正常？百思不得其解...
    over_picture_path = 'F://2017//12//ELTD//Constract//Constract_%s.jpg' %number_id       # 改变亮度、对比度后的图片image1

    # 疑问：是在对比度/亮度处理前的图片上显示故障特征还是在对比度处理后的图片image1上显示故障特征？
    # 我这里写的是后者。
    bounding_show(new_contours,need_deal_el,number_id)       # 在image1 中展示故障特征
    save_bounding_picture(new_contours,need_deal_el,number_id,
                          constract_el_path,rectangle_el_path)            # 根据轮廓，提取故障特征保存在本地

