from pydantic import BaseModel, Field

from app.domains.entities.text import Text


class Audio(BaseModel):
    speed: int = Field(gt=0, default=1)
    text: str
    project_id: int

    class Config:
        orm_mode = True


class AudioDetail(BaseModel):
    speed: int
    project_id: int
    texts: list[Text] = []

    class Config:
        orm_mode = True
