from pydantic import BaseModel

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
