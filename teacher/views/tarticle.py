from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from teacher import models
from utils.pagination import Pagination
from teacher.form import LoginForm, RegisterModelForm,ArticleForm


# Create your views here.
# 验证装饰器
def check_login(func):
    def warpper(request, *args, **kwargs):
        is_login = request.session.get('is_login', False)
        if is_login:
            return func(request, *args, **kwargs)
        else:
            return redirect('/teacher/login')

    return warpper


def loginpage(request):
    login_form = LoginForm()
    register_form = RegisterModelForm()
    content = {
        'login_form': login_form,
        'register_form': register_form,
    }
    return render(request, 'teacher/login_page.html', content)


@csrf_exempt
def signin(request):
    form = LoginForm(data=request.POST)
    if form.is_valid():

        user_obj = models.UserInfo.objects.filter(**form.cleaned_data).first()
        if not user_obj:
            form.add_error('password', '用户名或密码错误')
            result = {'status': False, 'errors': form.errors}
            return JsonResponse(result)

        request.session['info'] = {'id': user_obj.id, 'name': user_obj.username, 'mobile': user_obj.mobile}
        request.session['is_login'] = True
        request.session.set_expiry(60 * 60 * 24 * 7)
        result = {'status': True}
        return JsonResponse(result)
    result = {'status': False, 'errors': form.errors}
    return JsonResponse(result)


@csrf_exempt
def register(request):
    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        user_obj = models.UserInfo.objects.filter(mobile=form.cleaned_data['mobile']).first()
        if user_obj:
            form.add_error('mobile', '手机号已存在，请重新输入')
            result = {'status': False, 'errors': form.errors}
            return JsonResponse(result)
        form.save()
        result = {'status': True}
        return JsonResponse(result)
    result = {'status': False, 'errors': form.errors}
    return JsonResponse(result)


@check_login
def index(request):
    return render(request, 'teacher/index.html')


def logout(request):
    request.session.clear()
    return redirect('/teacher/loginpage')

@csrf_exempt
@check_login
def article_add(request):
    form = ArticleForm()
    if request.method == 'GET':
        return render(request, 'teacher/article_add.html', locals())
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
    queryset = models.TeacherArticles.objects.filter(**data_dict).order_by("update_time")
    if queryset:
        page_obj = Pagination(request, queryset, page_size=20, plus=3)
        page_queryset = page_obj.page_queryset
        page_string = page_obj.html()
        prama_dict = {
            'value': value,
            'page_queryset': page_queryset,
            'page_string': page_string
        }
        return render(request, "teacher/article_list.html", prama_dict)
    return render(request, "teacher/article_list.html")


def article_edit(request, nid):
    article_obj = models.TeacherArticles.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = ArticleForm(instance=article_obj)
        return render(request, "teacher/article_edit.html", {'form': form})
    form = ArticleForm(data=request.POST, instance=article_obj)
    if form.is_valid():
        detail_str = request.POST.get('detail', '')
        title_str = detail_str.split('\n')[0]
        form.instance.title = title_str
        form.save()
        return redirect("/teacher/article/list")
    return render(request, "teacher/article_edit.html", {'form': form})


def article_delete(request, nid):
    models.TeacherArticles.objects.filter(id=nid).delete()
    return redirect('/teacher/article/list')

