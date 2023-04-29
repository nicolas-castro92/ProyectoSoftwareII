from pydantic import BaseModel
from typing import Optional


class UserSchema(BaseModel):
    id: Optional[int]
    name: str
    last_name: str
    identification_card: int
    age: int
    phone: int
    email: str
    password: Optional[str]
    address: str 