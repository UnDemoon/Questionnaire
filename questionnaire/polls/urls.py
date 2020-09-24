from django.urls import path

from . import views, views_admin

urlpatterns = [
    path('management/', views.index, name='management'),
    path('visit/', views.visit, name='visit'),
    path('result/', views.result, name='result'),
    path('login/', views_admin.login, name='login'),
    path('questionnaireList/', views_admin.questionnaireList, name='questionnaireList'),
]