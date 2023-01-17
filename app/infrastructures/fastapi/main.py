from fastapi import FastAPI

from app.infrastructures.fastapi.router import router
from app.infrastructures.settings import ApplicationSettings
from app.infrastructures.containers import ApplicationContainer


def create_app() -> FastAPI:
    container = ApplicationContainer()
    container.config.from_pydantic(ApplicationSettings())

    container.wire(packages=['app.controllers'])
    container.audio_package.wire(packages=['app.controllers'])

    db = container.db()
    db.create_database()

    app = FastAPI()

    app.mount(container.config.static_url(), container.static(), name='static')
    app.mount(container.config.media_url(), container.media(), name='media')

    app.container = container
    app.include_router(router)

    return app


app = create_app()
