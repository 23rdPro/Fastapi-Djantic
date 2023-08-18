from django.contrib import admin
from django.urls import path

from fastapi import APIRouter
from blog.blog_app.api.views import users, posts


router = APIRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
]
