from pydantic import BaseModel


class Project(BaseModel):
    title: str

    class Config:
        orm_mode = True
