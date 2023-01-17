from sqlalchemy import Column, ForeignKey, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.infrastructures.database.orm import Model
from app.infrastructures.database.main import Base


class Model(Base):
    ...


class AudioModel(Model):
    __tablename__ = 'audio'

    id = Column(Integer, primary_key=True)
    speed = Column(Integer, default=1)
    project_id = Column(Integer, ForeignKey("project.id"))
    updated_at = Column(DateTime, default=datetime.now())
    is_converted = Column(Boolean, default=False)

    texts = relationship("TextModel", back_populates="audio",
                         order_by="asc(TextModel.index)", cascade='all,delete', lazy='selectin')
    project = relationship("Project", back_populates="audios", lazy='selectin')


class ProjectModel(Model):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    title = Column(String, default='')
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    audios = relationship("AudioModel", back_populates="project",
                          cascade='all,delete', lazy='selectin')


class TextModel(Model):
    __tablename__ = 'text'

    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    content = Column(Text)
    audio_id = Column(Integer, ForeignKey("audio.id"))
    UniqueConstraint(audio_id, index)

    audio = relationship("AudioModel", back_populates="texts", lazy='selectin')
