import os,re
def filerename(path):
    filelist=os.listdir(path)   #该文件夹下所有的文件（包括文件夹）
    for files in filelist:      #遍历所有文件
        Olddir=os.path.join(path,files)      #原来的文件路径
        if os.path.isdir(Olddir):            #如果是文件夹则跳过
            continue
        if '月' in Olddir:
            filename=os.path.splitext(files)[0]  #文件名
            filetype=os.path.splitext(files)[1]  #文件扩展名
            matching = re.compile(r'\d+\s')
            middle_i = matching.findall(filename)
            new_i = middle_i[0].strip(' ')+middle_i[1].strip(' ')+middle_i[2].strip(' ')+middle_i[3].strip(' ')+middle_i[4].strip(' ')+middle_i[5].strip(' ')+filetype
            Newdir=os.path.join(path,new_i)   #新的文件路径
            os.rename(Olddir,Newdir)   #重命名
        else:
            break
    return ('文件重命名成功')