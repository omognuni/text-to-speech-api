from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base

class Project(Base):
    __tablename__ = 'project'
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    
    audios = relationship("Audio", back_populates="project", cascade='all,delete')