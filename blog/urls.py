from django.contrib import admin
from django.urls import path

from fastapi import APIRouter, status
from blog.blog_app.api.views import users, posts


router = APIRouter()

router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    summary="Create new oser",
    tags=['users', ]
)(users.create_user)

urlpatterns = [
    path('admin/', admin.site.urls),
]
