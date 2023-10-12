from fastapi import APIRouter, Depends

from server.db import get_db, get_database
from typing import List, Annotated
from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

import uuid

from motor.motor_asyncio import AsyncIOMotorClient

from fastapi import Depends, HTTPException, status

from .model import User, UserIN, Token, TokenData

import os


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

SECRET_KET=os.getenv("SECRET_KEY","SECRET_KEY")
ALGORITHM=os.getenv("HASHING_ALGORITHM","HS256")
ACCESS_TOKEN_EXPIRE_MINUTES=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES",30)

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "Pets": "Read Pets."},
    )

def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_context.hash(password)

def get_user(username: str, db):
    # users = db.users.find()
    print("in get_user",username)
    print("in get_db",db)
    if username in db:
        user_dict = db[username]
        return User(**user_dict)

def authenticate_user(username: str, password: str, db):
    # users = db.users.find()
    user = get_user(username,db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KET, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncIOMotorClient = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate":"Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    users = db.users.find()
    user = get_user(username= token_data.username, db=users)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# def find_user_by_username(username):


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db : AsyncIOMotorClient = Depends(get_database)):
    # print(db)
    print("in token")
    users = db.users.find()
    print(f"Got this users {users}")

    user = authenticate_user(form_data.username, form_data.password, db=users)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate":"Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub":user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# @router.get("/")
# async def get_users(token: Annotated[str, Depends(oauth2_scheme)]):
#     pass 


# @router.post("/add")
# async def add_user():
#     pass

# @router.put("/update")
# async def update_user():
#     pass

# @router.delete("/delete")
# async def delete_user():
#     pass

@router.get("/me", response_model=User)
async def get_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.get("/me/pet", response_model=User)
async def read_adopted_pet(current_user: User = Depends(get_current_active_user)):
    return current_user.adopted_petID

@router.post("/add", response_model=UserIN)
async def add_user(userin: UserIN, db: AsyncIOMotorClient = Depends(get_database)) -> User:
    user_ret = User(**userin.dict(), userID=str(uuid.uuid4()), created_at=datetime.now(), updated_at=datetime.now())
    await db.users.insert_one(user_ret.dict())
    return user_ret