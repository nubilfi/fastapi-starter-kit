"""
Main file to run the app
"""
from os import getenv
import sys
sys.path.extend(["./"])

#pylint: disable=wrong-import-position
from app.main import app
from app.routes.basic import router as basic_router
from app.routes.cars import router as cars_router
from app.routes.authors import router as authors_router
from app.routes.books import router as books_router
from app.config import set_dotenv
#pylint: enable=wrong-import-position

set_dotenv()

ROUTERS = (basic_router, cars_router, authors_router, books_router)

app.include_router(ROUTERS[0], tags=["Basic"])
app.include_router(ROUTERS[1], tags=["Cars"])
app.include_router(ROUTERS[2], tags=["Authors"])
app.include_router(ROUTERS[3], tags=["Books"])

if __name__ == "__main__":
    import uvicorn

    #  Options: 'critical', 'error', 'warning', 'info', 'debug', 'trace'.
    uvicorn.run("app.main:app", host=getenv('APP_HOST'),
                port=int(getenv('APP_PORT')), reload=True, log_level="debug")
