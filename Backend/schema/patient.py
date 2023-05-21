from pydantic import BaseModel
from typing import Optional

class UserPatientFamiliarView(BaseModel):
    user_id: int
    name: str
    last_name: str
    identification_card: str
    age: int
    phone: str
    email: str
    address: str
    patient_id: int
    familiar_id: Optional[int]
    familiar_name: Optional[str]
    familiar_last_name: Optional[str]
    familiar_identification_card: Optional[str]
    familiar_age: Optional[int]
    familiar_phone: Optional[str]
    familiar_email: Optional[str]
    familiar_address: Optional[str]
    familiar_alternate_phone: Optional[str]

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
    familiar_id: Optional[int]
    

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
