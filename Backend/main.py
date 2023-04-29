from fastapi import FastAPI
from router.user_router import user
from router.patient_router import patient

app = FastAPI()

app.include_router(user)


# INSTANCIA CASOS DE USO ITERACION 1
# caso de uso Jose-Davids, aqui instancia el router
# caso de uso Estefania-Nicolas, aqui instancia el router
app.include_router(patient)

