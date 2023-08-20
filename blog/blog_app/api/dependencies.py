from asgiref.sync import sync_to_async
from blog import prefix
from django.conf import settings
from django.contrib.auth.models import User
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'{prefix}/token')
oauth = Depends(oauth2_scheme)
KEY = settings.env("KEY")  # openssl rand -hex 32


async def get_user(token: Annotated[str, oauth]):
    http_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = await sync_to_async(jwt.decode)(
            token, KEY, algorithms=['HS256']
        )
        username = payload.get("sub")

        if not await User.objects.afilter(
                username=username).aexists():
            raise http_exception

    except JWTError:
        raise http_exception

    return await User.objects.aget(username=username)


user_obj = Depends(get_user)


async def get_active_user(user: Annotated[User, user_obj]):
    if user.is_active:
        return user
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Inactive User")


active_user_obj = Depends(get_active_user)
