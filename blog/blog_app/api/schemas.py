from enum import IntEnum
from djantic import ModelSchema
from pydantic import BaseModel
from blog.blog_app.models import Post
from django.contrib.auth.models import User


class EnumStatusSchema(IntEnum):
    Draft = 0
    Publish = 1


class StatusSchema(BaseModel):
    Draft: EnumStatusSchema = EnumStatusSchema.Draft
    Publish: EnumStatusSchema = EnumStatusSchema.Publish


class UserSchema(ModelSchema):
    class Config:
        model = User
        include = ['username', 'password', 'email']


class PostSchema(ModelSchema):
    author: UserSchema
    status: EnumStatusSchema

    class Config:
        model = Post
        include = ['title', 'slug', 'author', 'created_on',
                   'updated_on', 'content', 'status', ]
