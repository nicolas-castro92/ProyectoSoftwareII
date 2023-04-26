from fastapi import FastAPI
from router.user_router import user

app = FastAPI()

app.include_router(user)