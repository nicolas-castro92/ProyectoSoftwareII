from pydantic import BaseModel

class UserFamiliarCreate(BaseModel):
    name: str
    last_name: str
    identification_card: str
    age: int
    phone: str
    email: str
    password: str
    address: str
    alternate_phone: str

class UserFamiliarView(BaseModel):
    id: int
    name: str
    last_name: str
    identification_card: str
    age: int
    phone: str
    email: str
    address: str
    familiar_id: int
    alternate_phone: str

class UserFamiliarViewAll(BaseModel):
    name: str
    last_name: str
    identification_card: str
    age: int
    phone: str
    email: str
    address: str
    alternate_phone: str

class UserFamiliarUpdate(BaseModel):
    name: str
    last_name: str
    identification_card: str
    age: int
    phone: str
    email: str
    address: str
    alternate_phone: str

class FamiliarBase(BaseModel):
    alternate_phone: str

class FamiliarCreate(FamiliarBase):
    user_id: int

class FamiliarUpdate(FamiliarBase):
    pass

class FamiliarView(FamiliarBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
