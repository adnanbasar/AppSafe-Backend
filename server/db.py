from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')
MONGODB_URL=f"mongodb+srv://{os.getenv('MONGO_USERNAME','')}:{os.getenv('MONGO_PASSWORD','')}@cluster0.{os.getenv('MONGO_DB_KEY','')}.mongodb.net/"


class Database:
	client: AsyncIOMotorClient = None

db = Database()

async def get_database() -> AsyncIOMotorClient:
	return db.client[MONGO_DB_NAME]


def get_db():
	return db.client[MONGO_DB_NAME]

def create_mongo_connection():
	print('Connecting to database...')
	db.client = AsyncIOMotorClient(
                f'{MONGODB_URL}'
        )
	print('Connected!')

def close_mongo_connection():
	print('Disconnecting from database...')
	db.client.close()
	print('Disconnected!')