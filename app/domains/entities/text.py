from pydantic import BaseModel, Field


class Text(BaseModel):
    index: int
    content: str

    class Config:
        orm_mode = True
