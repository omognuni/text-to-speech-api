from abc import ABC, abstractmethod
from typing import Tuple, List
from pydantic import BaseModel


class TextRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[BaseModel]:
        raise NotImplementedError

    @abstractmethod
    def get_by_index(self, model: BaseModel) -> BaseModel:
        raise NotImplementedError

    @abstractmethod
    def create(self, model: BaseModel) -> BaseModel:
        raise NotImplementedError

    @abstractmethod
    def update(self, instance_id, model: BaseModel) -> BaseModel:
        raise NotImplementedError

    @abstractmethod
    def delete(self, instance_id: int) -> None:
        raise NotImplementedError
