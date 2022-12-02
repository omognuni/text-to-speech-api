from fastapi import FastAPI

from router import router
from settings import ApplicationSettings
from containers import ApplicationContainer

def create_app() -> FastAPI:
    container = ApplicationContainer()
    container.config.from_pydantic(ApplicationSettings())
    
    container.wire(packages=['api'])
    container.audio_package.wire(packages=['api'])
    
    db = container.db()
    db.create_database()
    
    app = FastAPI()
       
    app.mount(container.config.static_url(), container.static(), name='static')
    app.mount(container.config.media_url(), container.media(), name='media')

    app.container = container
    app.include_router(router)
    
    return app

app = create_app()