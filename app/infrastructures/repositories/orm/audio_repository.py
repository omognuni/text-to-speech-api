from typing import Callable, ContextManager, Tuple
from sqlalchemy.orm import Session

from infrastructures.exceptions import NotFoundError
from infrastructures.repositories.repository import AbstractRepository


class AudioRepository(AbstractRepository):
    
    
    def __init__(self, model: Model, session_factory: Callable[..., ContextManager[Session]], media_root: str = '') -> None:
        self.model = model
        self.session_factory = session_factory
        self.media_root = media_root
    
    
    def _folder(self, audio_id):
        return os.path.join(self.media_root, f'{audio_id}')

  
    def get_all(self):
        with self.session_factory() as session:
            return session.query(self.model).all()

    def get_or_create(self, **kwargs):
        with self.session_factory() as session:
            instance = session.query(self.model).filter_by(**kwargs).first()
            if instance:
                return instance
            else:
                instance = self.model(**kwargs)
                session.add(instance)
                session.commit()
                session.refresh(instance)
            return instance

    def get_by_id(self, instance_id: int):
        with self.session_factory() as session:
            instance = session.query(self.model).filter(
                self.model.id == instance_id).first()
            if not instance:
                raise NotFoundError(instance_id)
            return instance

    def add(self, **kwargs):
        with self.session_factory() as session:
            instance = self.model(**kwargs)
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return instance

    def update(self, instance_id, **kwargs):
        with self.session_factory() as session:
            instance = session.query(self.model).filter(
                self.model.id == instance_id).first()
            for k, v in kwargs.items():
                setattr(instance, k, v)
            return instance

    def delete(self, instance_id: int):
        with self.session_factory() as session:
            instance = session.query(self.model).filter(
                self.model.id == instance_id).first()
            if not instance:
                raise NotFoundError(instance_id)
            session.delete(instance)
            session.commit()

    def get_by_id(self, audio_id: int):
        with self.session_factory() as session:
            instance = session.query(self.model).filter(
                self.model.id == audio_id).join(AudioText).first()
            if not instance:
                raise NotFoundError(audio_id)
            return instance

    def delete(self, audio_id: int):
        with self.session_factory() as session:
            audio = session.query(self.model).filter(
                self.model.id == audio_id).first()
            if not audio:
                raise NotFoundError(audio_id)
            session.delete(audio)
            session.commit()
            shutil.rmtree(os.path.join(self._folder(audio_id)))
        return

    def get_media(self, audio_id: int):
        try:
            path = shutil.make_archive(self._folder(audio_id), 'zip', self._folder(audio_id) )
            return path
        except FileNotFoundError:
            return
