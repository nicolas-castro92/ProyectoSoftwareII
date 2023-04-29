
from router.medical_staff_router import medical_staff
from fastapi import FastAPI
from router.user_router import user
from router.familiar_router import familiar
from router.patient_router import patient

app = FastAPI()

app.include_router(user)

# INSTANCIA CASOS DE USO ITERACION 1
app.inculde_router(medical_staff)
app.include_router(familiar)
app.include_router(patient)

