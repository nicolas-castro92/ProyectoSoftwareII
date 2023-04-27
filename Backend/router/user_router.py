from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_409_CONFLICT
from schema.user_schema import UserSchema
from config.db import engine
from model.user import users

user = APIRouter()


@user.post("/api/user", status_code=HTTP_201_CREATED)
def create_user(data_user: UserSchema):
    with engine.connect() as conn:
        # Check if the ID is already in the database
        query = users.select().where(users.c.identification_card == data_user.identification_card)
        result = conn.execute(query)
        existing_user = result.fetchone()

        if existing_user:
            # Return an HTTP 409 Conflict response if the ID already exists
            return Response(status_code=HTTP_409_CONFLICT,content="User already exists")

        # Insert the new user if the ID is not already in the database
        nuevo = data_user.dict()
        conn.execute(users.insert().values(nuevo))
        conn.commit()

    # Return an HTTP 201 Created response if the user was successfully created
    return Response(status_code=HTTP_201_CREATED)
