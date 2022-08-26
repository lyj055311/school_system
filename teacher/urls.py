from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from .views import tarticle,sarticle,smanage

urlpatterns = [
    path('loginpage', tarticle.loginpage),
    path('signin', tarticle.signin),
    path('register', tarticle.register),
    path('index', tarticle.index),
    path('logout', tarticle.logout),

    path('article/add', tarticle.article_add),
    path('article/list', tarticle.article_list),
    path('article/<int:nid>/edit', tarticle.article_edit),
    path('article/<int:nid>/delete', tarticle.article_delete),

    path('article/statistics',sarticle.article_statistics),
    path('s_article/<int:nid>/view',sarticle.s_article_view),
    path('s_article/<int:nid>/delete',sarticle.s_article_delete),
    path('article/chart/', sarticle.chart),
    path('article/chart2/', sarticle.chart2),

    path('s_list', smanage.student_list),
    path('s_batch', smanage.student_batch),
    path('s_clear', smanage.student_clear),
]
