from django.shortcuts import render
import os,datetime,re
from djangoapp import models,cnn,filerename
from django.http import HttpResponse
import requests,json
from django import forms
# Create your views here.
def homepage(request):
    return render(request, 'homepage.html')

# dashboard仪表盘 页面
def index(request):
    return render(request,'index.html')
def blank(request):
    return render(request,'blank.html')
def cards(request):
    return render(request,'cards.html')
def charts(request):
    return render(request,'charts.html')
def forgotpassword(request):
    return render(request, 'forgotpassword.html')
def login(request):
    return render(request, 'login.html')
def navbar(request):
    return render(request, 'navbar.html')
def register(request):
    return render(request, 'navbar.html')
def tables(request):
    return render(request, 'tables.html')

def upload(request):
    if request.method == 'GET':
        return render(request,'upload.html')
    elif request.method == 'POST':
        # 请求api的结果
        url = 'http://restapi.amap.com/v3/ip?key=b55e49c33bd3a93081481980973aefab&'
        x = requests.get(url)
        out = x.json()['province'] + x.json()['city']

        obj = request.FILES.getlist('pic')
        count = 0
        for i in obj:
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
            models.NewTable.objects.create(Datetime=date, Path=path,RenamePath = repath)
        return render(request,'prediction.html',{'count':count,'out':out})

def result(request):
    counts = request.GET.get('ids')
    int_counts = int(counts)
    c = []
    content = models.NewTable.objects.all().values('RenamePath').order_by('-id')[:int_counts]  # 从数据库取数据
    for i in content:
        c.append(i['RenamePath'])
    # y = 'F:/untitled/media/pexpy.155.jpg'
    context = {
        'picture_path': content,
        'result': cnn.prediction(c)
    }
    # models.NewTable.objects.create(Tag=context['result'])
    #models.NewTable.objects.all().order_by('-id').update(Tag = context['result'])
    index = 0
    for j in content:
        #and i in range(len(content)):
        models.NewTable.objects.filter(RenamePath=j['RenamePath']).update(Tag=context['result'][index])
        index += 1
    return render(request,'result.html',context)

def test(request):
    if request.method == 'POST':
        pictures = models.NewTable.objects.all().order_by('-id')[10:12]
        return render(request, 'test.html', {'pictures': pictures})
    if request.method == 'GET':
        result = request.GET.get('malfunction','None')      # 此值可看作是 每张照片里的故障特征描述  初始值为空，在这里，由于采用预加载图片的形式，所以test.html一刷新就会有初始值传递到数据库中。

        # 👇测试数据库
        models.Test.objects.create(test_char=result,test_number = 5)   # 选择结果存到数据库中
        pictures = models.NewTable.objects.all().order_by('-id')
        el_images = []
        all_el_images = []
        for i in pictures:
            el_images.append(i.RenamePath)
            all_el_images.append(i.Path)
        # 1.视图函数中的字典或列表要用 json.dumps()处理(序列化处理)。2.在模板上要加 safe 过滤器。
        return render(request, 'test.html', {'result': result, 'el_images': json.dumps(el_images),'all_el_images':json.dumps(all_el_images)})


