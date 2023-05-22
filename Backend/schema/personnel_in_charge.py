from pydantic import BaseModel

class PersonalACargoSchema(BaseModel):
    id: int
    patient_id: int
    medical_staff_id: int

    class Config:
        orm_mode = True