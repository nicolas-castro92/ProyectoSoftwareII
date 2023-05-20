from fastapi import FastAPI
from router.user import router as user_router
from router.familiar import router as familiar_router

app = FastAPI()

# Routers
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(familiar_router, prefix="/familiars", tags=["familiars"])

