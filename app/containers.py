from dependency_injector import containers, providers
from pydantic import BaseSettings, Field

from database import Database

from audio.containers import AudioContainer


class DatabaseSettings(BaseSettings):
    url: str = Field(default="sqlite:///", env='DATABASE_URL')

class ApplicationSettings(BaseSettings):
    db = DatabaseSettings()
    
class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.from_pydantic(ApplicationSettings())
    
    db = providers.Singleton(Database, db_url=config.db.url)
    
    audio_package = providers.Container(
        AudioContainer,
        db = db,
    )