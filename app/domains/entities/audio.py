from sqlalchemy import Column, ForeignKey, Integer, Text, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Audio(Base):
    __tablename__ = 'audio'
    
    id = Column(Integer, primary_key=True)
    speed = Column(Integer, default=1)
    project_id = Column(Integer, ForeignKey("audio_project.id"))
    updated_at = Column(DateTime, default=datetime.now())
    
    texts = relationship("AudioText", back_populates="audio", order_by="asc(AudioText.index)", cascade='all,delete')
    project = relationship("AudioProject", back_populates="audios")


class AudioText(Base):
    __tablename__ = 'audio_text'
    
    id = Column(Integer, primary_key=True)
    index = Column(Integer, unique=True)
    content = Column(Text)
    audio_id = Column(Integer, ForeignKey("audio.id"))
    
    audio = relationship("Audio", back_populates="texts")
    
class AudioProject(Base):
    __tablename__ = 'audio_project'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, default='')
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    
    audios = relationship("Audio", back_populates="project", cascade='all,delete')