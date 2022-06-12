# app/urls.py

from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('nuevo_prestamo', views.nuevo_prestamo, name='nuevo_prestamo'),
  path('nuevo_libro', views.nuevo_libro, name='nuevo_libro'),
  path('test_template', views.test_template, name='test_template'),
]
