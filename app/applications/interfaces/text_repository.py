from abc import ABC, abstractmethod
from typing import List
from pydantic import BaseModel
from app.domains.entities import Text


class TextRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Text]:
        raise NotImplementedError

    @abstractmethod
    def get_by_index(self, model: BaseModel) -> Text:
        raise NotImplementedError

    @abstractmethod
    def create(self, model: BaseModel) -> Text:
        raise NotImplementedError

    @abstractmethod
    def update(self, instance_id, model: BaseModel) -> Text:
        raise NotImplementedError

    @abstractmethod
    def delete(self, instance_id: int) -> None:
        raise NotImplementedError
