from sqlalchemy import Column, ForeignKey, Integer, DateTime, Boolean, Text, String, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.infrastructures.database.main import Base


class Audio(Base):
    __tablename__ = 'audio'

    id = Column(Integer, primary_key=True)
    speed = Column(Integer, default=1)
    project_id = Column(Integer, ForeignKey("project.id"))
    updated_at = Column(DateTime, default=datetime.now())
    is_converted = Column(Boolean, default=False)

    texts = relationship("Text", back_populates="audio",
                         order_by="asc(Text.index)", cascade='all,delete', lazy='selectin')
    project = relationship("Project", back_populates="audios", lazy='selectin')


class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    title = Column(String, default='')
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    audios = relationship("Audio", back_populates="project",
                          cascade='all,delete', lazy='selectin')


class Text(Base):
    __tablename__ = 'text'

    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    content = Column(Text)
    audio_id = Column(Integer, ForeignKey("audio.id"))
    UniqueConstraint(audio_id, index)

    audio = relationship("Audio", back_populates="texts", lazy='selectin')
