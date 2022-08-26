from django.db import models


# Create your models here.
class StudentInfo(models.Model):
    class Meta:
        verbose_name_plural = '学生信息'

    class_room = models.CharField(verbose_name='班级', max_length=64)
    name = models.CharField(verbose_name='姓名', max_length=32)
    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)
    identitycard = models.CharField(verbose_name='身份证号', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    def __str__(self):
        return self.name


class StudentArticles(models.Model):
    title = models.CharField(verbose_name='标题', max_length=64)
    detail = models.TextField(verbose_name='内容')
    author = models.ForeignKey(verbose_name='作者', to='StudentInfo', to_field='id', on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
