from pydantic import BaseModel, Field

from app.controllers.schemas.text import TextSchema


class AudioSchema(BaseModel):
    speed: int = Field(gt=0, default=1)
    text: str
    project_id: int

    class Config:
        orm_mode = True


class AudioDetailSchema(BaseModel):
    speed: int
    project_id: int
    texts: list[TextSchema] = []

    class Config:
        orm_mode = True
