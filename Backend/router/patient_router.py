from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_409_CONFLICT
from schema.patient_schema import PatientSchema
from config.db import engine
from model.patient import patients

patient = APIRouter()


@patient.post("/api/patient", status_code=HTTP_201_CREATED)
async def create_patient(data_patient: PatientSchema):
    with engine.connect() as conn:
        query = patients.select().where(patients.c.user_id == data_patient.user_id)
        result =  conn.execute(query)
        existing_patient =  result.fetchone()

        if existing_patient:
            return Response(status_code=HTTP_409_CONFLICT,content="Patient already exists")

        nuevo = data_patient.dict()
        conn.execute(patients.insert().values(nuevo))
        conn.commit()

    return  Response(status_code=HTTP_201_CREATED)