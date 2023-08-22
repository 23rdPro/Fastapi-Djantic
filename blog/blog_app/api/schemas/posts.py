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
    status: EnumStatusSchema

    class Config:
        model = Post
        include = ['title', 'content', 'status', ]


class UpdatePostSchema(ModelSchema):
    status: EnumStatusSchema or None = None

    class Config:
        model = Post
        include = ["title", "content", "status"]


class DisplayPostSchema(ModelSchema):
    author: UserSchema
    status: int

    class Config:
        model = Post
        include = ['title', 'content', 'status', 'slug',
                   'created_on', 'updated_on', 'author']
