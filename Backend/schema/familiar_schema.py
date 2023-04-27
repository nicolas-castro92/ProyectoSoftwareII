from pydantic import BaseModel
from typing import Optional


class FamiliarSchema(BaseModel):
    id: Optional[int]
    alternate_phone: str
