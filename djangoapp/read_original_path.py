import os,shutil,re
'''
重命名 未修改

f = open(os.path.join('F:/untitled/media',i.name),'wb')
for line in i.chunks():
    f.write(line)
    f.close()
    count += 1
    path = os.path.join('F:/untitled/media',i.name).replace('\\', '/')
    date = datetime.datetime.now()      # 时间戳
    models.Table.objects.create(Datetime=date,Path=path)

    # 只是对路径重命名，还未解决文件重命名的问题
    matching = re.compile(r'\d+\s')
    middle_i = matching.findall(i.name)
    new_i = middle_i[0].strip(' ')+middle_i[1].strip(' ')+middle_i[2].strip(' ')+middle_i[3].strip(' ')+middle_i[4].strip(' ')+middle_i[5].strip(' ')+'.'+i.name.split('.')[1]
    repath = 'F:/untitled/media/'+new_i
    # 对文件重命名
    os.rename(path, repath)
'''

# 提取图片
path_list = []
dir = "E://EL分类10月-总//"
for i in os.listdir(dir):
    dir1 = os.path.join(dir,i)
    for j in os.listdir(dir1):
        if j == 'L4':
            dir2 = os.path.join(dir1, j)
            for k in os.listdir(dir2):
                dir3 = os.path.join(dir2,k)
                path_list.append(dir3)
                '''
                for m in os.listdir(dir3):
                    if '.jpg' in m:
                        image_path = os.path.join(dir3,m)
                        #print(image_path)
                    elif 'Thumbs' in m:
                        continue
                    elif '新建文件夹' in m:
                        dir4 = os.path.join(dir3,m)
                        for n in os.listdir(dir4):
                            new_image_path = os.path.join(dir4,n)
                            print(new_image_path)
                '''


# 移动到指定文件夹
#os.chdir(test_list[0])
target_path = "F:\\data\\EL picture\\移动测试"
def copy_file(imagepath):
    for each_file in os.listdir(imagepath):
        if 'Thumbs.db' not in each_file:
            if os.path.isfile(os.path.join(imagepath,each_file)) :
                #if 'jpg' in each_file:
                shutil.copy(os.path.join(imagepath,each_file), target_path + "\\" + each_file)  # 复制文件至指定路径
                #print("Copy file from %s to %s " % (os.getcwd() +'\\' + each_file, target_path + "\\" + each_file))
            else:
                imagepath = imagepath+'\\'+each_file
                copy_file(imagepath)


# 在指定文件夹内把图片统一移动到指定文件夹REnamepath下
# 再把 REnamepath文件夹下的文件重命名，以后opencv处理的图像从这个REnamepath文件夹下获取

for i in os.listdir(target_path):
    file_path = os.path.join(target_path,i)
    new_file_path = 'F://2017//12//REnamepath'+'//'+i

    # 把图片从"F:\\data\\EL picture\\移动测试"复制到 'F://2017//12//REnamepath'路径下
    shutil.copyfile(file_path,new_file_path)

for i in os.listdir('F://2017//12//REnamepath'):
    file_path = os.path.join('F://2017//12//REnamepath',i)
    matching = re.compile(r'\d+\s')
    middle_i = matching.findall(i)
    new_i = middle_i[0].strip(' ') + middle_i[1].strip(' ') + middle_i[2].strip(' ') + middle_i[3].strip(' ') + middle_i[4].strip(' ') + middle_i[5].strip(' ') + '.' + i.split('.')[1]
    repath = 'F://2017//12//REnamepath//' + new_i
    print(new_i)
    os.rename(file_path,repath)
    #os.remove(file_path)



if __name__ == '__main__':
    '''
      nohslist = []
    for i in path_list:
        if '划伤' not in i:
            nohslist.append(i)

    for j in nohslist:
        copy_file(j)
    '''
