from typing import Callable, ContextManager, Tuple, List
from sqlalchemy.orm import Session

from app.applications.interfaces.repository import AbstractRepository
from app.domains.entities.text import Text
from app.infrastructures.database.orm import TextModel


class TextRepository(AbstractRepository):
    def __init__(self, session_factory: Callable[..., ContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self) -> List[TextModel]:
        with self.session_factory() as session:
            return session.query(TextModel).all()
        ...

    def get_or_create(self, text: Text) -> Tuple(bool, Text):
        with self.session_factory() as session:
            text = session.query(TextModel).filter_by()
        ...

    # def get_by_id(self, instance_id: int) -> Text:
    #     with self.session_factory() as session:

    #     ...

    # def create(self, **kwargs) -> Text:
    #     with self.session_factory() as session:

    #     ...

    # def update(self, instance_id, **kwargs) -> Text:
    #     with self.session_factory() as session:

    #     ...

    # def delete(self, instance_id: int) -> None:
    #     with self.session_factory() as session:

    #     ...
