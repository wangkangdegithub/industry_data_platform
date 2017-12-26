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

class NewTable(models.Model):
    Datetime = models.DateTimeField()
    Path = models.CharField(max_length=30)
    Tag = models.CharField(max_length=30)
    RenamePath = models.CharField(max_length=30)

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return self.Path
