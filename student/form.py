from django import forms
from django.core.validators import RegexValidator
from . import models
from utils.bootstrap import BootStrapModelForm, BootStrapForm
from utils.encrypt import md5


class StudentLoginForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['password']

    class Meta:
        model = models.StudentInfo
        fields = ['name', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-box'}),
            'password': forms.PasswordInput(attrs={'class': 'input-box', 'placeholder': '密码：学籍号后六位'})
        }

    def clean_password(self):
        pwd = self.cleaned_data['password']
        return md5(pwd)


class ArticleForm(forms.ModelForm):
    class Meta:
        model = models.StudentArticles
        fields = ['detail']
