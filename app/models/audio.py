from sqlalchemy import Column, ForeignKey, Integer, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base


class Audio(Base):
    __tablename__ = 'audio'
    
    id = Column(Integer, primary_key=True)
    speed = Column(Integer, default=1)
    project_id = Column(Integer, ForeignKey("project.id"))
    updated_at = Column(DateTime, default=datetime.now())
    
    texts = relationship("AudioText", back_populates="audio", order_by="asc(AudioText.index)", cascade='all,delete')
    project = relationship("Project", back_populates="audios")


class AudioText(Base):
    __tablename__ = 'audio_text'
    
    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    content = Column(Text)
    audio_id = Column(Integer, ForeignKey("audio.id"))
    
    audio = relationship("Audio", back_populates="texts")