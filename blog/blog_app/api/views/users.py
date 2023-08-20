import datetime

from asgiref.sync import sync_to_async
from blog.blog_app.api.helpers import (
    create_user_sync,
    to_schema,
    create_token_sync,
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
    if not await sync_to_async(authenticate)(form.username, form.password):
        raise http_exception
    if not await User.objects.aget(username=form.username).is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Inactive user")
    token_expires = datetime.timedelta(weeks=1)
    data = {'sub': form.username}
    token = await create_token_sync(data, expires_delta=token_expires)
    token_data = {'access_token': token,
                  'token_type': 'bearer',
                  }
    return TokenModel(**token_data)


async def logout():
    pass


async def get_users():
    pass


async def get_user():
    pass


async def me():
    pass


async def update_me():
    pass


async def delete_me():
    pass
