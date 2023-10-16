from django.contrib import admin
from django.urls import path,include
from Hello import views

urlpatterns = [
    path('',views.index,name='hello'),
    path('upload/', views.upload, name='upload'),
    path('result/', views.result, name='result'),
    path('pie_chart/', views.pie_chart, name='pie_chart')
]
