from fastapi import FastAPI
from router.user_router import user
from router.medical_staff_router import medical_staff


app = FastAPI()

app.include_router(user)
app.include_router(medical_staff)

# INSTANCIA CASOS DE USO ITERACION 1
# caso de uso Jose-Davids, aqui instancia el router
# caso de uso Estefania-Nicolas, aqui instancia el router
# caso de uso Alejandro, aqui instancia el router

