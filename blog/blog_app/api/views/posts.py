from typing import Annotated

from blog.blog_app.api.dependencies import active_user_dependency
from blog.blog_app.api.schemas.posts import PostSchema
from django.contrib.auth.models import User


async def create_post(user: Annotated[User, active_user_dependency], schema: PostSchema):
    pass


async def get_posts():
    pass


async def get_post():
    pass


async def get_user_posts():
    pass


async def get_user_post():
    pass


async def update_post_me():
    pass


async def delete_post_me():
    pass
