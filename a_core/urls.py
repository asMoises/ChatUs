from django.contrib import admin
from django.urls import path
from a_home.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
]
