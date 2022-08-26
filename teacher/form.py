from django.core.exceptions import ValidationError
from django import forms
from utils.bootstrap import BootStrapModelForm, BootStrapForm
from utils.encrypt import md5
from django.core.validators import RegexValidator
from . import models


class LoginForm(BootStrapForm):
    mobile = forms.CharField(label='手机号', widget=forms.TextInput(),
                             validators=[RegexValidator(r'^1\d{10}$', '错误：请输入正确的的11位手机号码')], )
    password = forms.CharField(label='密码', widget=forms.PasswordInput(render_value=True))

    def clean_password(self):
        pwd = self.cleaned_data['password']
        return md5(pwd)


class RegisterModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码', widget=forms.PasswordInput(render_value=True))
    mobile = forms.CharField(label='手机号',
                             validators=[RegexValidator(r'^1\d{10}$', '错误：请输入正确的的11位手机号码')], )

    class Meta:
        model = models.UserInfo
        fields = ['username', 'mobile', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True)
        }

    def clean_confirm_password(self):
        pwd = self.cleaned_data['password']
        confirm = md5(self.cleaned_data['confirm_password'])
        if pwd != confirm:
            raise ValidationError('密码不一致:重新输入')
        else:
            return pwd  # confirm_password保存到数据库的值

    def clean_password(self):
        pwd = self.cleaned_data['password']
        return md5(pwd)


class ArticleForm(forms.ModelForm):
    class Meta:
        model = models.TeacherArticles
        fields = ['detail']
