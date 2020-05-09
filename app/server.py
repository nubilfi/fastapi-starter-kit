"""
Main file to run the app
"""
from os import getenv
import sys
sys.path.extend(["./"])

#pylint: disable=wrong-import-position
from starlette.middleware.cors import CORSMiddleware

from app.main import app
from app.routes.api_v1.api import routers
from app.config import set_dotenv
#pylint: enable=wrong-import-position

set_dotenv()

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers, prefix=getenv("API_PREFIX"))

if __name__ == "__main__":
    import uvicorn

    #  Options: 'critical', 'error', 'warning', 'info', 'debug', 'trace'.
    uvicorn.run("app.main:app", host=getenv('APP_HOST'),
                port=int(getenv('APP_PORT')), reload=True, log_level="debug")
