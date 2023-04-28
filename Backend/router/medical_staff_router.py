from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_409_CONFLICT
from schema.medical_stafff_schema import MedicalStaffSchema
from config.db import engine
from model.medical_staff import medical_staffs
from schema.user_schema import UserSchema
from model.user import users
import secrets


medical_staff = APIRouter()


@medical_staff.post("/api/medical_staffs", status_code=HTTP_201_CREATED)
async def create_medical_staff(data_medical_staff: MedicalStaffSchema, data_user: UserSchema):
    with engine.connect() as conn:
        # Verificar si ya existe un registro con la misma clave profesional
        query = medical_staffs.select().where(medical_staffs.c.professional_card == data_medical_staff.professional_card)
        result = conn.execute(query)
        existing_medical_staff = result.fetchone()
        if existing_medical_staff:
            return Response(status_code=HTTP_409_CONFLICT, content="This Medical staff already exists")
        # Crear un nuevo usuario
        nuevo_usuario = data_user.dict()
        password = secrets.token_hex(16)  # Generar contraseña aleatoria
        nuevo_usuario['password'] = password
        query = users.insert().values(nuevo_usuario)
        result = conn.execute(query)
        user_id = result.lastrowid

        # Crear un nuevo registro de médico y vincularlo con el usuario creado
        nuevo_medico = data_medical_staff.dict()
        nuevo_medico['user_id'] = user_id
        conn.execute(medical_staffs.insert().values(nuevo_medico))

        conn.commit()

    return {"id": user_id, "password": password} ,Response(status_code=HTTP_201_CREATED)

 