from pydantic import BaseSettings, Field


class DatabaseSettings(BaseSettings):
    url: str = Field(env='DATABASE_URL')

class ApplicationSettings(BaseSettings):
    db = DatabaseSettings()
    static_root: str  = Field(default='/vol/web/static')
    media_root: str = Field(default='/vol/web/media')
    static_url: str = Field(default='/static/staic/')
    media_url: str = Field(default='/static/media/')