from pydantic import BaseModel, Field


class TextSchema(BaseModel):
    index: int = Field(gt=0)
    audio_id: int
    content: str

    class Config:
        orm_mode = True
