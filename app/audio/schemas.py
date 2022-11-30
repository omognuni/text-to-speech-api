from pydantic import BaseModel, Field


class ProjectSchema(BaseModel):
    title: str

class AudioSchema(BaseModel):
    speed: int = Field(gt=0, default=1)
    text: str
    project_id: int
    
class AudioTextSchema(BaseModel):
    index: int
    content: str
    
    class Config:
        orm_mode = True
    
class AudioDetailSchema(BaseModel):
    speed: int
    project_id: int
    texts: list[AudioTextSchema] = []
    
    class Config:
        orm_mode = True
    