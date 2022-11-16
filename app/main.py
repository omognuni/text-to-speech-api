from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from router import router

import db
import config

app = FastAPI()

app.include_router(router)

app.mount("/static/static", StaticFiles(directory=config.STATIC_ROOT), name='static')
app.mount("/static/media", StaticFiles(directory=config.MEDIA_ROOT), name='media')

db.Base.metadata.create_all(bind=db.engine)