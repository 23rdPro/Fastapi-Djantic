import re

from typing import Union

from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# from django.utils.translation import gettext_lazy as _
from djantic import ModelSchema
from pydantic import BaseModel


@sync_to_async
def to_schema(orm, schema_cls: Union[ModelSchema, BaseModel]):
    return schema_cls.from_orm(orm)


@sync_to_async
def create_user_sync(**kwargs):
    # regex is in two parts, negative lookahead: ?!.* and
    # chars not alphanumeric
    ptn = re.compile(r'^(?!.*[^\dA-Za-z]).*$', re.I)
    if re.match(ptn, kwargs.get("username")) is None:
        raise ValidationError("username only accepts alphanumeric")
    elif User.objects.filter(username=kwargs.get('username')).exists():
        raise ValidationError('username already exists')
    pwd_ptn = re.compile(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
        re.I
    )
    if re.match(pwd_ptn, kwargs.get('password')) is None:
        raise ValidationError("""
        password must contain at least 8 characters,
        at least one uppercase letter,
        one lowercase letter,
        one number and one special character
        """)
    return User.objects.create_user(**kwargs)
