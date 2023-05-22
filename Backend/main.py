from fastapi import FastAPI
from router.user import router as user_router
from router.familiar import router as familiar_router
from router.medical_staff import router as medical_staff_router
from router.patient import router as patient_router
app = FastAPI()

# Routers
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(familiar_router, prefix="/familiars", tags=["familiars"])
app.include_router(medical_staff_router, prefix="/medical_staff", tags=["medical_staff"])
app.include_router(patient_router, prefix="/patients", tags=["patients"])

