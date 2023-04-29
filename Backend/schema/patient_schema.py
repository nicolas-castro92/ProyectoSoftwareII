from pydantic import BaseModel
from typing import Optional
from sqlalchemy import ForeignKey

class PatientSchema(BaseModel):
    id: Optional[int]
    familiar_id: int 
    user_id: int 