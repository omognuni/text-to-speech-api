from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from router import router
from containers import ApplicationContainer

# import db
import config

def create_app() -> FastAPI:
    container = ApplicationContainer()
    
    db = container.db()
    db.create_database()
    
    app = FastAPI()
    
    app.mount("/static/static", StaticFiles(directory=config.STATIC_ROOT), name='static')
    app.mount("/static/media", StaticFiles(directory=config.MEDIA_ROOT), name='media')

    app.container = container
    app.include_router(router)
    return app

app = create_app()