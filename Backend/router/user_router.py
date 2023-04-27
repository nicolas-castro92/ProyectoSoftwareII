from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED
from schema.user_schema import UserSchema
from config.db import conn
from model.user import users

user = APIRouter()

@user.post("/api/user", status_code=HTTP_201_CREATED)
def create_user(data_user: UserSchema):
    nuevo = data_user.dict()
    conn.execute(users.insert().values(nuevo))
    conn.commit()
    print(data_user)
    print(nuevo)
    return Response(status_code=HTTP_201_CREATED)
