import os

from dependency_injector import containers, providers
from pydantic import BaseSettings, Field
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import ScopedSession


class DatabaseSettings(BaseSettings):
    url: str = Field(default="sqlite:///", env='DATABASE_URL')

class ApplicationSettings(BaseSettings):
    db = DatabaseSettings()
    
class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    engine = providers.Singleton(create_engine, url=config.db.url)
    session = providers.Singleton(sessionmaker, bind=engine)