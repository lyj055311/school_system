from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from teacher import models
from utils.pagination import Pagination
from teacher.form import LoginForm, RegisterModelForm, ArticleForm
from student.models import StudentInfo, StudentArticles
from student.form import ArticleForm


def article_statistics(request):
    class_value = request.GET.get('class_room', '')
    search_value = request.GET.get('q', '')
    class_queryset = StudentInfo.objects.values("class_room").distinct()

    article_queryset = StudentArticles.objects.all()

    if class_value:
        article_queryset = StudentArticles.objects.filter(author__class_room=class_value)
        # 统计每一条学生数据对应的文章数量
        article_chart_student = StudentInfo.objects.filter(class_room=class_value).annotate(
            count=Count('studentarticles__id'))
        # print(article_chart_student)
    # 统计每一个班的文章数量
    atiticle_chart_class = StudentInfo.objects.values('class_room').annotate(count=Count('studentarticles__id'))
    # print(atiticle_chart_class)

    if search_value:
        article_queryset = StudentArticles.objects.filter(
            Q(author__class_room__icontains=search_value) | Q(title__icontains=search_value) | Q(
                author__name__icontains=search_value))

    if article_queryset:
        article_page_obj = Pagination(request, article_queryset, page_size=20, plus=3)
        article_page_queryset = article_page_obj.page_queryset
        article_page_string = article_page_obj.html()
        prama_dict = {
            'class_queryset': class_queryset,
            'article_page_queryset': article_page_queryset,
            'article_page_string': article_page_string,

        }
        return render(request, 'teacher/article_statistics.html', prama_dict)
    return render(request, "teacher/article_statistics.html", {'class_queryset': class_queryset, })


def s_article_view(request, nid):
    article_obj = StudentArticles.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = ArticleForm(instance=article_obj)
        return render(request, "teacher/article_edit.html", {'form': form})
    form = ArticleForm(data=request.POST, instance=article_obj)
    if form.is_valid():
        detail_str = request.POST.get('detail', '')
        title_str = detail_str.split('\n')[0]
        form.instance.title = title_str
        form.save()
        return redirect("/teacher/article/statistics")
    return render(request, "teacher/article_edit.html", {'form': form})


def s_article_delete(request, nid):
    StudentArticles.objects.filter(id=nid).delete()
    return redirect('/teacher/article/statistics')


def chart(request):
    article_chart_class = StudentInfo.objects.values('class_room').annotate(count=Count('studentarticles__id'))

    xdata_list = []
    ydata_list = []

    for value_dict in article_chart_class:
        xdata_list.append(value_dict['count'])
        ydata_list.append(value_dict['class_room'])
    # print(ydata_list)
    result = {
        'status': True,
        'xdata': xdata_list,
        'ydata': ydata_list,
    }

    return JsonResponse(result)


def chart2(request):
    class_value = request.GET.get('class_room', '')
    article_chart = StudentInfo.objects.filter(class_room=class_value).annotate(
        count=Count('studentarticles__id'))
    xdata_list = []
    ydata_list = []

    for obj in article_chart:
        xdata_list.append(obj.count)
        ydata_list.append(obj.name)
    result = {
        'status': True,
        'xdata': xdata_list,
        'ydata': ydata_list,
    }
    return JsonResponse(result)
