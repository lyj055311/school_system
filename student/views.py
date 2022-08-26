from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from utils.pagination import Pagination
from . import models
from .form import StudentLoginForm, ArticleForm


# Create your views here.
# 自定义登录验证装饰器
def check_login(func):
    def warpper(request, *args, **kwargs):
        is_login = request.session.get('is_login', False)
        if is_login:
            return func(request, *args, **kwargs)
        else:
            return redirect('/student/login')

    return warpper


def login(request):
    if request.method == 'GET':
        form = StudentLoginForm()
        return render(request, 'student/login.html', {'form': form})
    form = StudentLoginForm(data=request.POST)
    if form.is_valid():
        student_obj = models.StudentInfo.objects.filter(**form.cleaned_data).first()
        if not student_obj:
            form.add_error('password', '用户名或密码错误')
            return render(request, 'student/login.html', {'form': form})
        request.session['info'] = {'id': student_obj.id, 'name': student_obj.name, 'class_room': student_obj.class_room,
                                   'card': student_obj.identitycard}
        request.session['is_login'] = True
        request.session.set_expiry(60 * 40)
        return redirect('/student/index')
    return render(request, 'student/login.html', {'form': form})


def logout(request):
    request.session.clear()
    return redirect('/student/login')


@check_login
def index(request):
    return render(request, 'student/index.html')


@csrf_exempt
@check_login
def article_add(request):
    form = ArticleForm()
    if request.method == 'GET':
        return render(request, 'student/article_add.html', locals())
    detail_str = request.POST.get('detail', '')
    title_str = detail_str.split('\n')[0]
    form = ArticleForm(data=request.POST)
    if form.is_valid():
        form.instance.title = title_str
        form.instance.author_id = int(request.session['info']['id'])
        form.save()
        context = {'status': True}
        return JsonResponse(context)
    context = {'status': False, 'errors': form.errors}
    return JsonResponse(context)


@check_login
def article_list(request):
    data_dict = {}
    value = request.GET.get('q', '')  # 如果不能获取到q的值就是空字符串
    if value:
        data_dict['title__contains'] = value
    data_dict['author_id'] = int(request.session['info']['id'])
    queryset = models.StudentArticles.objects.filter(**data_dict).order_by("update_time")
    if queryset:
        page_obj = Pagination(request, queryset, page_size=20, plus=3)
        page_queryset = page_obj.page_queryset
        page_string = page_obj.html()
        prama_dict = {
            'value': value,
            'page_queryset': page_queryset,
            'page_string': page_string
        }
        return render(request, "student/article_list.html", prama_dict)
    return render(request, "student/article_list.html")


def article_edit(request, nid):
    article_obj = models.StudentArticles.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = ArticleForm(instance=article_obj)
        return render(request, "student/article_edit.html", {'form': form})
    form = ArticleForm(data=request.POST, instance=article_obj)
    if form.is_valid():
        detail_str = request.POST.get('detail', '')
        title_str = detail_str.split('\n')[0]
        form.instance.title = title_str
        form.save()
        return redirect("/student/article/list")
    return render(request, "student/article_edit.html", {'form': form})


def article_delete(request, nid):
    models.StudentArticles.objects.filter(id=nid).delete()
    return redirect('/student/article/list')
