from blog.blog_app.api.helpers import create_user_sync, to_schema
from blog.blog_app.api.schemas.users import UserSchema
from fastapi import Depends


async def create_user(schema: UserSchema = Depends()):
    user = await create_user_sync(**schema.dict())
    return await to_schema(user, UserSchema)


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
