from django.db import models

# Create your models here.
class UserInfo(models.Model):
    username=models.CharField(verbose_name='姓名',max_length=32)
    password=models.CharField(verbose_name='密码',max_length=64)
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    def __str__(self):
        return self.username

class TeacherArticles(models.Model):
    title = models.CharField(verbose_name='标题', max_length=64)
    detail = models.TextField(verbose_name='内容')
    author = models.ForeignKey(verbose_name='作者', to='UserInfo', to_field='id', on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)