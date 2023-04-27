from pydantic import BaseModel
from typing import Optional
from sqlalchemy import ForeignKey

class FamiliarSchema(BaseModel):
    id: Optional[int]
    alternate_phone: str
