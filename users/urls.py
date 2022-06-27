from django.contrib import admin
from django.urls import path, re_path
from application import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import permissions
from rest_framework_swagger.views import get_swagger_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/<int:id>', views.API.delete_or_put),
    path('posts/', views.API.get_post)
]

#urlpatterns = format_suffix_patterns(urlpatterns)
