from asgiref.sync import sync_to_async
from typing import Annotated

from blog.blog_app.api.dependencies import active_user_dependency
from blog.blog_app.api.helpers import get_posts_me_sync, to_schema
from blog.blog_app.api.schemas.posts import PostSchema, DisplayPostSchema, UpdatePostSchema
from blog.blog_app.models import Post
from django.contrib.auth.models import User
from fastapi import Depends, HTTPException, status

from blog.blog_app.api.helpers import to_schema_many


async def create_post_me(
        user: Annotated[User, active_user_dependency],
        schema: PostSchema = Depends(),
):
    d = schema.dict()
    title = await sync_to_async(Post.objects.filter)(title=d['title'])
    if await title.aexists():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Title already exists")
    d['status'] = d['status'].value
    d.update({'author': user})
    p = Post(**d)
    await sync_to_async(p.save)()
    return await sync_to_async(DisplayPostSchema.from_orm)(p)


async def get_posts(user: Annotated[User, active_user_dependency]):  # noqa
    # get all posts
    posts = await sync_to_async(Post.objects.all)()
    return await sync_to_async(DisplayPostSchema.from_django)(posts, many=True)


async def get_posts_me(user: Annotated[User, active_user_dependency]):  # noqa
    # get all posts by me
    posts = await get_posts_me_sync(user.username)
    return await to_schema_many(posts, DisplayPostSchema)


async def post(
        user: Annotated[User, active_user_dependency],   # noqa
        post_id: int
):
    p = await sync_to_async(Post.objects.filter)(pk=post_id)
    return await to_schema(await p.aget(), DisplayPostSchema)


async def update_post_me(
        user: Annotated[User, active_user_dependency],  # noqa
        post_id: int,
        schema_cls: UpdatePostSchema = Depends()
):
    p = await sync_to_async(Post.objects.filter)(pk=post_id)
    cls = schema_cls.dict(exclude_none=True, exclude_unset=True, exclude_defaults=True)
    if await p.aexists():
        await p.aupdate(**cls)
        # await sync_to_async(p.save)()
        return await to_schema(await p.aget(), DisplayPostSchema)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')


async def delete_post_me(user: Annotated[User, active_user_dependency],  # noqa
                         post_id: int):
    p = await sync_to_async(Post.objects.filter)(pk=post_id)
    if await p.aexists():
        await sync_to_async(p.delete)()
        return {'ok': True}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')
