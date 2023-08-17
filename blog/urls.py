from django.contrib import admin
from django.urls import path

from fastapi import APIRouter
from blog_app.api import views

router = APIRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
]
