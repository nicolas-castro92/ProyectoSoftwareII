from fastapi import FastAPI
from router.user import router as user_router

app = FastAPI()

# Routers
app.include_router(user_router, prefix="/users", tags=["users"])

