from enum import IntEnum
from djantic import ModelSchema
from pydantic import BaseModel
from blog.blog_app.models import Post

from .users import UserSchema


class EnumStatusSchema(IntEnum):
    Draft = 0
    Publish = 1


class StatusSchema(BaseModel):
    Draft: EnumStatusSchema = EnumStatusSchema.Draft
    Publish: EnumStatusSchema = EnumStatusSchema.Publish


class PostSchema(ModelSchema):
    author: UserSchema
    status: EnumStatusSchema

    class Config:
        model = Post
        include = ['title', 'slug', 'author', 'created_on',
                   'updated_on', 'content', 'status', ]
