import uvicorn
import os

DEV = os.getenv('DEV', False)

if __name__ == '__main__':
	uvicorn.run('server.app:app', host='0.0.0.0', port=8000 if DEV else 8001, reload=True)