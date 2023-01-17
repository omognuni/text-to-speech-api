from abc import ABC, abstractmethod
from typing import Tuple, List
from pydantic import BaseModel


class ProjectRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[BaseModel]:
        raise NotImplementedError

    @abstractmethod
    def get_or_create(self, model: BaseModel) -> Tuple(bool, BaseModel):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, instance_id: int) -> BaseModel:
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
