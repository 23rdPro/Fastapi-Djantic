# from __future__ import annotations

import datetime

from asgiref.sync import sync_to_async
from blog.blog_app.api.dependencies import user_dependency, active_user_dependency
from blog.blog_app.api.helpers import (
    create_user_sync,
    to_schema,
    create_token_sync,
    validate_u_regex,
)
from blog.blog_app.api.schemas.users import UserSchema
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from fastapi import Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

from blog.blog_app.api.schemas.token import TokenModel


async def create_user(schema: UserSchema = Depends()):
    user = await create_user_sync(**schema.dict())
    return await to_schema(user, UserSchema)


async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    http_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not await sync_to_async(authenticate)(
            username=form.username, password=form.password
    ):
        raise http_exception
    user = await User.objects.aget(username=form.username)
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Inactive user")
    token_expires = datetime.timedelta(weeks=1)
    data = {'sub': form.username}
    token = await create_token_sync(data, expires_delta=token_expires)
    token_data = {'access_token': token,
                  'token_type': 'bearer',
                  }
    return TokenModel(**token_data)


async def get_users(user: Annotated[User, active_user_dependency]):  # noqa
    users = User.objects.all()
    return await sync_to_async(UserSchema.from_django)(users, many=True)


async def me(user: Annotated[User, user_dependency]):
    return await to_schema(user, UserSchema)


async def update_me(user: Annotated[User, user_dependency], schema: UserSchema or None = None):
    # partial update
    u = await sync_to_async(User.objects.filter)(pk=user.pk)
    s_data = schema.dict(
        exclude_none=True,
        exclude_defaults=True,
        exclude_unset=True
    )
    if await u.aexists() and await sync_to_async(validate_u_regex)(**s_data):
        await u.aupdate(**s_data)
    u = await u.aget()
    return await sync_to_async(UserSchema.from_orm)(u)


async def delete_me(user: Annotated[User, user_dependency]):
    u = await sync_to_async(User.objects.filter)(pk=user.pk)
    if await u.aexists():
        await sync_to_async(u.delete)()
        # handle auth revoke todo
        return {'ok': True}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="user not found")
