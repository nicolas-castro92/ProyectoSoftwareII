from pydantic import BaseModel
from typing import Optional
from schema.user_schema import UserSchema

#Esquema para personal medico
class MedicalStaffSchema(BaseModel):
    professional_card: int
    specialty: str
    personal_type: str
    user_id: Optional[int]
    