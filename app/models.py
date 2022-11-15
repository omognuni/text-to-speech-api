from sqlalchemy import Column, ForeignKey, String, Integer, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base


class Audio(Base):
    __tablename__ = 'audio'
    
    id = Column(Integer, primary_key=True)
    updated_at = Column(DateTime, default=datetime.now())
    speed = Column(Integer, default=1)
    project_id = Column(Integer, ForeignKey("project.id"))
    
    texts = relationship("AudioText", back_populates="audio", order_by="asc(AudioText.index)", cascade='all,delete')
    project = relationship("Project", back_populates="audios")

    
class Project(Base):
    __tablename__ = 'project'
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    
    audios = relationship("Audio", back_populates="project", cascade='all,delete')
    
    
class AudioText(Base):
    __tablename__ = 'audio_text'
    
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    index = Column(Integer)
    audio_id = Column(Integer, ForeignKey("audio.id"))
    
    audio = relationship("Audio", back_populates="texts")