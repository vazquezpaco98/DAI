# mi_sitio_web/urls.py

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
  url('admin/', admin.site.urls),
  url('', include('app.urls')),
]