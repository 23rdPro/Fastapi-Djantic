from django.contrib import admin
from django.urls import path

from fastapi import APIRouter, status
from blog.blog_app.api.views import users, posts


router = APIRouter()


router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    summary="create new oser",
    tags=['users', ]
)(users.create_user)

router.post(
    "/token",
    status_code=status.HTTP_200_OK,
    summary="authenticate user",
    tags=['users', ]
)(users.login)

router.get(
    "/users/me",
    status_code=status.HTTP_200_OK,
    tags=['users', ],
    summary="get current user"
)(users.me)

router.get(
    '/users',
    status_code=status.HTTP_200_OK,
    summary='get all users',
    tags=['users', ]
)(users.get_users)

router.delete(
    '/users/me/delete',
    status_code=status.HTTP_200_OK,
    tags=['users', ],
    summary="delete user"
)(users.delete_me)

router.patch(
    '/users/me/update',
    status_code=status.HTTP_200_OK,
    tags=['users', ],
    summary="update user"
)(users.update_me)

router.post(
    '/posts',
    status_code=status.HTTP_201_CREATED,
    summary='create post',
    tags=['posts']
)(posts.create_post_me)

router.get(
    '/posts',
    status_code=status.HTTP_200_OK,
    summary='get all posts',
    tags=['posts']
)(posts.get_posts)

router.delete(
    '/posts/{post_id}/delete',
    status_code=status.HTTP_200_OK,
    summary='delete post me',
    tags=['posts']
)(posts.delete_post_me)

router.patch(
    '/posts/{post_id}/update',
    status_code=status.HTTP_200_OK,
    tags=['posts'],
    summary='update post me'
)(posts.update_post_me)

router.get(
    '/posts/me',
    status_code=status.HTTP_200_OK,
    summary='get all posts by me',
    tags=['posts']

)(posts.get_posts_me)

router.get(
    '/posts/{post_id}',
    status_code=status.HTTP_200_OK,
    summary='view single post',
    tags=['posts']
)(posts.post)


urlpatterns = [
    path('admin/', admin.site.urls),
]
