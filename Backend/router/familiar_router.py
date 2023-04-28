from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_409_CONFLICT
from schema.familiar_schema import FamiliarSchema
from config.db import engine
from model.familiar import familiars

familiar = APIRouter()


@familiar.post("/api/familiar", status_code=HTTP_201_CREATED)
async def create_user(data_user: FamiliarSchema):
    with engine.connect() as conn:
        query = familiars.select().where(users.c.user_id == data_user.user_id)
        result =  conn.execute(query)
        existing_user =  result.fetchone()

        if existing_user:
            return Response(status_code=HTTP_409_CONFLICT,content="Familiar already exists")

        nuevo = data_user.dict()
        conn.execute(familiars.insert().values(nuevo))
        conn.commit()

    return  Response(status_code=HTTP_201_CREATED)
 