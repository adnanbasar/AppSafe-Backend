import os
from fastapi import FastAPI
from .db import create_mongo_connection, close_mongo_connection

from .modules.pets.routes import router as pet_router
from .modules.user.routes import router as user_router


app = FastAPI(
    title="AppSafe API",
    description="End to End API interface for AppSafe application",
    docs_url="/",
)

app.add_event_handler("startup", create_mongo_connection)
app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(
	pet_router,
	prefix='/pets',
	tags=['Pets'],
)

app.include_router(
	user_router,
	prefix='/users',
	tags=['Users'],
)


