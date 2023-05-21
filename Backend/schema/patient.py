from pydantic import BaseModel
from typing import Optional


class UserPatientViewAll(BaseModel):
    name: str
    last_name: str
    identification_card: str
    age: int
    phone: str
    email: str
    address: str

class UserPatientCreate(BaseModel):
    name: str
    last_name: str
    identification_card: str
    age: int
    phone: str
    email: str
    address: str
    familiar_id: Optional[int]


class UserPatientView(BaseModel):
    id: int
    name: str
    last_name: str
    identification_card: str
    age: int
    phone: str
    email: str
    address: str

class UserPatientUpdate(BaseModel):
    name: str
    last_name: str
    identification_card: str
    age: int
    phone: str
    email: str
    address: str

class PatientBase(BaseModel):
    familiar_id: int
    user_id: int

class PatientCreate(PatientBase):
    pass

class PatientUpdate(PatientBase):
    pass

class PatientView(PatientBase):
    id: int

    class Config:
        orm_mode = True
