from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_409_CONFLICT
from schema.user_schema import UserSchema
from config.db import engine
from model.user import users

user = APIRouter()


@user.post("/api/user", status_code=HTTP_201_CREATED)
async def create_user(data_user: UserSchema):
    with engine.connect() as conn:
        query = users.select().where(users.c.identification_card == data_user.identification_card)
        result =  conn.execute(query)
        existing_user =  result.fetchone()

        if existing_user:
            return Response(status_code=HTTP_409_CONFLICT,content="User already exists")

        nuevo = data_user.dict()
        conn.execute(users.insert().values(nuevo))
        conn.commit()

    return  Response(status_code=HTTP_201_CREATED)
 