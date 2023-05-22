from pydantic import BaseModel

class PersonalInChargeSchema(BaseModel):
    id: int
    patient_id: int
    medical_staff_id: int

    class Config:
        orm_mode = True