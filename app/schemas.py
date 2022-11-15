from pydantic import BaseModel, Field


class Audio(BaseModel):
    speed: int = Field(gt=0, default=1)
    text: str
    project_id: int
    
class AudioText(BaseModel):
    index: int
    content: str
    
    class Config:
        orm_mode = True
    
class AudioDetail(BaseModel):
    speed: int
    project_id: int
    texts: list[AudioText] = []
    
    class Config:
        orm_mode = True
    
class Project(BaseModel):
    title: str
    