from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params, paginate
from server.db import get_db, get_database
from server.modules.pets.model import Pet, PetIN, PetStatusUpdate
from motor.motor_asyncio import AsyncIOMotorClient
import uuid
from datetime import datetime
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("", response_model=Page[Pet])
async def get_pets(
    params: Params = Depends(),
    db: AsyncIOMotorClient = Depends(get_db)
) -> Page[Pet]:
    ret = db.pets.find().sort('updated_at',-1)
    ret = [i async for i in ret]
    return paginate(ret, params)

@router.post("/add", response_model=Pet)
async def add_pet(
    petin: PetIN, 
    db: AsyncIOMotorClient = Depends(get_database)
    ) -> Pet:
    pet_ret = Pet(petID=str(uuid.uuid4()),created_at=datetime.now(),updated_at=datetime.now(),**petin.dict())
    await db.pets.insert_one(pet_ret.dict())
    return pet_ret

@router.patch("/status-update/{petID}", response_model=Pet)
async def update_pet(petID: str, petupdatestatus: PetStatusUpdate, db: AsyncIOMotorClient = Depends(get_database)):
    pet_ret = await db.pets.find_one({"petID":petID})
    if pet_ret is None:
        return JSONResponse(status_code=404, content={"message": "pet not found"})
    pet_ret = Pet(**pet_ret)
    pet_ret.is_adopted = petupdatestatus.is_adopted
    pet_ret.adopted_by = petupdatestatus.adopted_by
    pet_ret.adopted_at = datetime.now()
    pet_ret.updated_at = datetime.now()
    await db.pets.update_one({"petID":petID},{"$set":pet_ret.dict()})
    return pet_ret

@router.delete("/delete/{petID}")
async def delete_pet(petID: str, db: AsyncIOMotorClient = Depends(get_database)):
    await db.pets.delete_one({"petID":petID})
    return JSONResponse(status_code=200, content={"message": "pet deleted"})

@router.get("/{petID}")
async def get_pet_info(petID: str, db: AsyncIOMotorClient = Depends(get_database))-> Pet:
    pet_ret = await db.pets.find_one({"petID":petID})
    if pet_ret is None:
        return JSONResponse(status_code=404, content={"message": "pet not found"})
    return Pet(**pet_ret)