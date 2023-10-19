import os
from fastapi import FastAPI
from .db import create_mongo_connection, close_mongo_connection
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

from .modules.pets.routes import router as pet_router
from .modules.user.routes import router as user_router

from .modules.user.model import User, UserIN, Token, TokenData
from .modules.user.routes import oauth2_scheme, get_current_user, authenticate_user, create_access_token

app = FastAPI(
    title="AppSafe API",
    description="End to End API interface for AppSafe application",
    docs_url="/",
)

app.add_middleware(HTTPSRedirectMiddleware)
# app.add_middleware(TrustedHostMiddleware, allowed_hosts=ALLOWED_HOSTS)
app.add_middleware(
    CORSMiddleware,
	allow_origins=ALLOWED_HOSTS,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
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
