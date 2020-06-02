from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auto_submit', views.auto_submit, name='auto_submit'),
]