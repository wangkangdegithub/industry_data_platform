# -*- coding: utf-8 -*-
# file: renamefile.py
# author: Wang Kang
# time: 12/28/2017 10:14 AM
# ----------------------------------------------------------------

import os,random

def renamefile(path,newname):
    """
    重命名故障特征文件夹里的文件名
    :param path: 各种故障特征文件夹路径
    :param newname: 文件名的新名字
    :return: 重命名后的故障文件路径（）
    """
    i = 0
    filelist=os.listdir(path)                               #该文件夹下所有的文件（包括文件夹）
    for files in filelist:                                  #遍历所有文件
        i += 1
        Olddir = os.path.join(path, files)                     #原来的文件路径
        if os.path.isdir(Olddir):                           #如果是文件夹则跳过
            continue
        filename = os.path.splitext(files)[0]                 #文件名
        filetype = os.path.splitext(files)[1]                 #文件扩展名
        Newdir = os.path.join(path, newname+str(i)+filetype)   #新的文件路径
        os.rename(Olddir, Newdir)                            #重命名
    print("故障特征重命名结束")
    return Newdir


def name_image_tag(train_dir):
    """
    给故障特征文件夹里的图片打标签（Y值），并对所有故障打乱顺序随机分布在变量中
    :param traindir: 各种故障特征文件夹路径的上级路径
    :return: 混洗后的打标签数据，可看作训练数据
    """
    # 故障列举不完整，还需要修改！
    train_pexpy = [(train_dir + i, 0) for i in os.listdir(train_dir) if 'pexpy' in i]
    train_xhhs = [(train_dir + i, 1) for i in os.listdir(train_dir) if 'xhhs' in i]
    train_md = [(train_dir + i, 2) for i in os.listdir(train_dir) if 'nmd' in i]
    train_data = train_pexpy + train_xhhs + train_md
    random.shuffle(train_data)
    return train_data



if __name__ == '__main__':
    path = 'D://Documents//Desktop//counters/'
    newname = 'szy'
    renamefile(path, newname)
