import os,cv2,random
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Input,Dropout,Flatten,Convolution2D,MaxPooling2D,ZeroPadding2D,Dense,Activation
from keras.optimizers import RMSprop,SGD
from keras.callbacks import ModelCheckpoint,Callback,EarlyStopping
from keras.utils import np_utils
from keras.models import load_model
from djangoapp import views
from djangoapp import models
rows = 64
cols = 64
channels = 1
def read_image(tuple_set):  # tuple_set 为 ('F:\\EL picture\\EL_trainxhhs.39.jpg', 1) 这种形式
    file_path = tuple_set[0]
    label = tuple_set[1]
    img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)  # 读灰度图,通过使用OpenCV进行读取
    return cv2.resize(img, (rows, cols), interpolation=cv2.INTER_CUBIC), label

def prep_data(images):
    no_images = len(images)
    data = np.ndarray((no_images,channels,rows,cols), dtype=np.uint8)    #‘tf’模式下，输入形如（samples，rows，cols，channels）的4D张量
    labels = []
    for i, image_file in enumerate(images):
        image, label = read_image(image_file)   #  image_file为 ('F:\\EL picture\\EL_train\\xhhs.39.jpg', 1) 这种形式
        data[i] = image
        labels.append(label)
    return data, labels

def prediction(dir):
    model = load_model('C:/Users/wangk/my_model_pe&md&xh&rw.h5')
    input_data = [(k, -1) for k in dir]
    middle_input_data = prep_data(input_data)[0]
    new_input_data = middle_input_data.transpose(0,3,2,1)
    result = np.argmax(model.predict(new_input_data), 1)

    # np_utils.to_categorical(int_labels) one-hot编码的label只能是 int()型
    '''
        for i in range(0, len(result)):
        if result[i] == 0:
            result[i] = str('PE吸盘印')
        elif result[i] == 1:
            result[i] = str('线痕划伤')
        elif result[i] == 2:
            result[i] = str('无规律麻点')
        else:
            result[i] = str('人为划伤')
    '''

    return result