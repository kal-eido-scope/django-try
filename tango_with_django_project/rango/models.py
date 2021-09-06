from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128,unique=True)     #charfield存字符串，max_length指定最大长度，unique指定
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    class Meta:
        verbose_name_plural = 'Categories'      #嵌套Meta类，修改复数情况名称
    def __str__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE) #Foreighkey是一对多，必须加on_delete
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    def __str__(self):
        return self.title