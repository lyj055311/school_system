from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('login', views.login),
    path('logout', views.logout),
    path('index',views.index),
    path('article/add',views.article_add),
    path('article/list',views.article_list),
    path('article/<int:nid>/edit',views.article_edit),
    path('article/<int:nid>/delete',views.article_delete),
]
