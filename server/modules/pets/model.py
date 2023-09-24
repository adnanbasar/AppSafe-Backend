# petID, name, age, breed, created_at, updated_at, is_adopted, adopted_by, adopted_at, deleted_at, 
# 

from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel

class BasePet(BaseModel):	
	class Config:
		use_enum_values = True
		
class Pet(BasePet):
    petID: str
    name: str
    immage: str | None = None
    age_in_months: int
    breed: str | None = None
    created_at: datetime
    updated_at: datetime
    is_adopted: bool = False
    adopted_by: str | None = None
    adopted_at: datetime | None = None 

class PetStatusUpdate(BasePet):
    is_adopted: bool
    adopted_by: str

class PetIN(BasePet):
    name: str
    immage: str | None = None
    age_in_months: int
    breed: str | None = None