from django.contrib.auth.models import User
from djantic import ModelSchema


class UserSchema(ModelSchema):
    class Config:
        model = User
        include = ['username', 'password']
