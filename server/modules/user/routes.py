from fastapi import APIRouter, Depends

from typing import List, Annotated
from fastapi.security import OAuth2PasswordBearer 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

@router.get("/")
async def get_users(token: Annotated[str, Depends(oauth2_scheme)]):
    pass


@router.post("/add")
async def add_user():
    pass

@router.put("/update")
async def update_user():
    pass

@router.delete("/delete")
async def delete_user():
    pass

@router.get("/me")
async def get_user_me():
    pass

