# mi_sitio_web/urls.py

from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
  url('admin/', admin.site.urls),
  url('', include('app.urls')),
  path('accounts/', include('allauth.urls')) # new
]