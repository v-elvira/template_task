from django.urls import path

from . import views

urlpatterns = [
    path('', views.other_index, name='index'),
    path('today_url', views.other_index, name='today'),
    path('<str:args>', views.other_index),
]