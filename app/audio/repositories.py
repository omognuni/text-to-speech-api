from typing import Callable, Iterator, ContextManager
from sqlalchemy.orm import Session

from audio.schemas import ProjectSchema, AudioSchema, AudioDetailSchema, AudioTextSchema

class BaseRepository:
    
    def __init__(self, model, schemas, session_factory: Callable[..., ContextManager[Session]]) -> None:
        self.model = model
        self.schemas = schemas
        self.session_factory = session_factory
        
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
            instance = session.query(self.model).filter(self.model.id == instance_id).first()
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
    
    def delete(self, instance_id: int):
        with self.session_factory() as session:
            instance = session.query(self.model).filter(self.model.id == instance_id).first()
            if not instance:
                raise NotFoundError(instance_id)
            session.delete(instance)
            session.commit()
    
class ProjectRepository(BaseRepository):
    pass

class AudioRepository(BaseRepository):
    pass

class AudioTextRepository(BaseRepository):
    pass

class NotFoundError(Exception):
    
    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} not found, id: {entity_id}")


#     def get_all(self):
#         with self.session_factory() as session:
#             return session.query(Project).all()
    
    
# class AudioRepo(BaseRepository):
#     def get_all(self):
#         with self.session_factory() as session:
#             return session.query(Project).all()
    
    
# class AudioTextRepo(BaseRepository):
#     def get_all(self):
#         return