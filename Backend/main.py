from fastapi import FastAPI
from router.user_router import user
from router.familiar_router import familiar

app = FastAPI()

app.include_router(user)

# INSTANCIA CASOS DE USO ITERACION 1
# caso de uso Jose-Davids, aqui instancia el router
app.include_router(familiar)
# caso de uso Alejandro, aqui instancia el router

