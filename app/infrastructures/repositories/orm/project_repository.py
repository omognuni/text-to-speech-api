from typing import Callable, ContextManager, Tuple
from sqlalchemy.orm import Session

from infrastructures.exceptions import NotFoundError
from infrastructures.repositories.repository import AbstractRepository


class ProjectRepository(AbstractRepository):
    
    def get_by_id(self, project_id: int):
        with self.session_factory() as session:
            instance = session.query(self.model).filter(
                self.model.id == project_id).first()
            if not instance:
                raise NotFoundError(project_id)
            return instance

    def delete(self, project_id: int):
        with self.session_factory() as session:
            project = session.query(self.model).filter(
                self.model.id == project_id).first()
            if not project:
                raise NotFoundError(project_id)
            session.delete(project)
            session.commit()

            for audio in project.audios:
                try:
                    shutil.rmtree(os.path.join(self._folder(audio.id)))
                except FileNotFoundError:
                    pass
        return

