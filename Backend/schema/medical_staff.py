from pydantic import BaseModel

class UserMedicalStaffCreate(BaseModel):
    name: str
    last_name: str
    identification_card: str
    age: int
    phone: str
    email: str
    address: str
    professional_card: str
    specialty: str
    personal_type: str

class UserMedicalStaffView(BaseModel):
    id: int
    name: str
    last_name: str
    identification_card: str
    age: int
    phone: str
    email: str
    address: str
    professional_card: str
    specialty: str
    personal_type: str

class UserMedicalStaffUpdate(BaseModel):
    name: str
    last_name: str
    identification_card: str
    age: int
    phone: str
    email: str
    address: str
    professional_card: str
    specialty: str
    personal_type: str

class MedicalStaffBase(BaseModel):
    professional_card: str
    specialty: str
    personal_type: str

class MedicalStaffCreate(MedicalStaffBase):
    user_id: int

class MedicalStaffUpdate(MedicalStaffBase):
    pass

class MedicalStaffView(MedicalStaffBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
