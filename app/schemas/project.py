from pydantic import BaseModel


class ProjectSchema(BaseModel):
    title: str
    
    class Config:
        orm_mode = True