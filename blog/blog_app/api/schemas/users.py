# from __future__ import annotations

from django.contrib.auth.models import User
from djantic import ModelSchema


class UserSchema(ModelSchema):
    username: str or None = ''
    password: str or None = ''

    class Config:
        model = User
        include = ['username', 'password']
