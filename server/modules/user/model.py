
# userID, name, role, email, password, created_at, updated_at, deleted_at, is_active, is_superuser, 
from datetime import datetime
from enum import Enum
from typing import List, Annotated

import secrets

from pydantic import BaseModel

class BaseUser(BaseModel):
    class Config:
        use_enum_values = True
        

class User(BaseUser):
    userID: str
    profile_picture: str = None
    name: str
    role: str | None = None
    email: str | None = None
    # hashed_password: str | None = None
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
    is_active: bool = True
    is_superuser: bool = False
    adopted_petID: str | None = None


class UserInDB(User):
    hashed_password: str

class UserIN(BaseUser):
    name: str
    role: str | None = None
    email: str | None = None
    password: str | None = None
    is_active: bool = True
    is_superuser: bool = False

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
    # role: str | None = None
