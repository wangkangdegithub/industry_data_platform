# -*- coding: utf-8 -*-
# file: whole_step.py
# author: Wang Kang
# time: 12/26/2017 23:16 PM
# ----------------------------------------------------------------

import cv2
import numpy as np
from tools import image_show
from adjust_light_contrast import light_contrast_coef,adjust_image_info
from draw_rectangle import draw_rectangle
from feature_extraction import *
from cnn import *
from renamefile import *

"""
1.根据标准图片调整待调图片          init_image-->original_image（image1）
"""
# 图片img的亮度系数、对比度系数
img = cv2.imread('D://Documents//Desktop//sxdhd.jpg')  # 标准图片
standard_light_coef = light_contrast_coef(img)[0]
standard_contrast_coef = light_contrast_coef(img)[1]
over_picture = adjust_image_info('D://Documents//Desktop//yycl2.jpg', standard_light_coef, standard_contrast_coef)


"""
2.调整后的图片画矩形边缘、格栅白线    image1-->image2
"""
add_rectangle_image = draw_rectangle(over_picture)


"""
3.通过图片image2进行故障特征的轮廓提取、并在original_image（image1）中展示故障特征
"""
# 为何直接调用变量add_rectangle_iamge 会报错？重新读路径正常？百思不得其解...
image = cv2.imread('D://Documents//Desktop//add_rectangle_image.jpg')      # 在image1的基础上增加矩形边缘、白色格栅线的图片image2
thresh = Contours_feature(image)[0]
transformed_image = transform_form(thresh, 'closing')
image_show('transformed_image',transformed_image)                          # 展示形态学转换后的二值图
new_image, new_contours, new_hierarchy = cv2.findContours(transformed_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)   # image2的二值图经过形态学转化后的轮廓等提取

# 为何直接调用变量over_picture 会报错？重新读路径正常？百思不得其解...
original_image = cv2.imread('D://Documents//Desktop//over_picture.jpg')    # 改变亮度、对比度后的图片image1
save_bounding_picture(new_contours, original_image)                        # 根据轮廓，提取故障特征保存在本地
bounding_show(new_contours, original_image)                                # 在image1 中展示故障特征


'''

"""
4.对提取出来的特征按类型存放不同文件夹下，并统一重命名、打标签
"""
path = 'D://Documents//Desktop//counters/'  # 各种故障特征文件夹路径
newname = 'szy'
renamefile(path, newname)
train_dir = ''                              # 各种故障特征文件夹路径的上级路径
train_data = name_image_tag(train_dir)


"""
5.提取出来的特征进行模型训练。
"""
test_images = train_data[:50]
train_images = train_data[50:]

# 训练模型需要用的调整参数-----------------------------------------
rows = 64
cols = 64
channels = 1
num_classes = 3
objective = 'categorical_crossentropy'
optimizer = RMSprop(lr=1e-3)
nb_epoch = 30
batch_size = 50
early_stopping = EarlyStopping(monitor='val_loss', patience=3, verbose=1, mode='auto')  # 当监测值不再改善时，该回调函数将中止训练
history = LossHistory()
# ----------------------------------------------------------------

x_train, y_train = prep_data(train_images, channels, rows, cols)
x_train = x_train.transpose(0, 3, 2, 1)                             # 训练输入转化为(样本数，64，64，通道channel)格式                                                  # 输出y 进行one-hot编码 n分类需要n个one-hot
y_train = np_utils.to_categorical(y_train, num_classes)

model = cnn_model(rows, cols, channels, num_classes, objective, optimizer)
model.fit(x_train, y_train, batch_size=batch_size, nb_epoch=nb_epoch, validation_split=0.2, verbose=1, shuffle=True,
          callbacks=[history, early_stopping])                      # 训练模型

# 观察学习曲线
loss = history.losses
val_loss = history.val_losses

plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('NN Loss Trend')
plt.plot(loss, 'blue', label='Training Loss')
plt.plot(val_loss, 'red', label='Validation Loss')
plt.xticks(range(0, nb_epoch)[0::2])
plt.legend()
plt.show()

# 测试集测试模型
x_test, y_test = prep_data(test_images)
x_test = x_test.transpose(0, 3, 2, 1)
y_test = np_utils.to_categorical(y_test, num_classes)

prediction = model.predict(x_test, verbose=1)
result = np.argmax(prediction, 1)
# 在测试集上的模型准确率
score = model.evaluate(x_test, y_test, verbose=1)
print(model.summary())

#model.save('modelname.h5')               # 训练好的模型保存到本地


"""
6.利用模型进行新数据预测。
"""
# 对新数据预测
need_predict_image_dir = ''
need_predict_image_result = prediction(need_predict_image_dir)

'''