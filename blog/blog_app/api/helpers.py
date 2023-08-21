import re
from datetime import datetime
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from jose import jwt
from django.conf import settings

KEY = settings.ENV('KEY')


@sync_to_async
def create_token_sync(data: dict, expires_delta):
    expire = datetime.utcnow() + expires_delta
    encode = data.copy()
    encode.update({'exp': expire})
    return jwt.encode(encode, KEY, algorithm='HS256')


@sync_to_async
def to_schema(orm, schema_cls):
    return schema_cls.from_orm(orm)


def validate_u_regex(**kwargs):
    # regex is in two parts, negative lookahead: ?!.* and
    # chars not alphanumeric
    ptn = re.compile(r'^(?!.*[^\dA-Za-z]).*$', re.I)
    pwd_ptn = re.compile(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
        re.I
    )

    if kwargs.get('username'):
        if re.match(ptn, kwargs.get("username")) is None:
            raise ValidationError("username only accepts alphanumeric")
        elif User.objects.filter(username=kwargs.get('username')).exists():
            raise ValidationError('username already exists')

    if kwargs.get('password'):
        if re.match(pwd_ptn, kwargs.get('password')) is None:
            raise ValidationError("""
            password must contain at least 8 characters,
            at least one uppercase letter,
            one lowercase letter,
            one number and one special character
            """)
    return True


@sync_to_async
def create_user_sync(**kwargs):
    if validate_u_regex(**kwargs):
        return User.objects.create_user(**kwargs)
