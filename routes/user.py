from fastapi import APIRouter
from models.user import User
from config.db import connection
from schema.user import serialize_dict, serialize_list
from bson import ObjectId
user = APIRouter()


@user.get('/')
async def get_all_users():
    return serialize_list(connection.local.user.find())


@user.post('/')
async def create_user(user_schema: User):
    connection.local.user.insert_one(dict(user_schema))
    return serialize_list(connection.local.user.find())


@user.put('/{id}')
async def update_user(user_id, user_data: User):
    connection.local.user.find_one_and_update({"_id": ObjectId(user_id)}, {
        "$set": dict(user_data)
    })
    return serialize_dict(connection.local.user.find_one({"_id": ObjectId(user_id)}))


@user.delete('/{id}')
async def delete_user(user_id):
    return serialize_dict(connection.local.user.find_one_and_delete({"id": ObjectId(user_id)}))
