from django.db import models

# Create your models here.
class ImageStore(models.Model):
    name = models.CharField(max_length=150,null=True)
    img = models.ImageField(upload_to='img')

class Person(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()

class Table(models.Model):
    Datetime = models.DateTimeField()
    Path = models.CharField(max_length=30)
    Tag = models.CharField(max_length=30)

# 包含重命名后的图片路径字段
class NewTable(models.Model):
    Datetime = models.DateTimeField()
    Path = models.CharField(max_length=30)
    Tag = models.CharField(max_length=30)
    RenamePath = models.CharField(max_length=30)

# 测试用的数据库，用来测试form表单提交的故障类结果
class Test(models.Model):
    test_char = models.CharField(max_length=30)
    test_number = models.IntegerField()


class TestELimg(models.Model):
    original_el_path = models.CharField(max_length=50)
    constract_el_path = models.CharField(max_length=50)
    rectangle_el_path = models.CharField(max_length=50)
    tzqt_el_path = models.CharField(max_length=50)
    dytzqt_el_path = models.CharField(max_length=50)
    dytz_el_path = models.CharField(max_length=50)
    el_type = models.CharField(max_length=50)

class TestELtype(models.Model):
    dytzqt_el_path = models.CharField(max_length=50,null=True)
    el_type = models.CharField(max_length=50)


    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return self.Path
