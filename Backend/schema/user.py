from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    last_name: str
    identification_card: str
    age: int
    phone: str
    email: str
    password: str
    address: str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserView(UserBase):
    id: int

    class Config:
        orm_mode = True
