from abc import ABC, abstractmethod
from typing import List
from pydantic import BaseModel
from app.domains.entities import Project


class ProjectRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[BaseModel]:
        raise NotImplementedError

    @abstractmethod
    def get_or_create(self, model: BaseModel) -> tuple[bool, Project]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, instance_id: int) -> BaseModel:
        raise NotImplementedError

    @abstractmethod
    def create(self, model: BaseModel) -> Project:
        raise NotImplementedError

    @abstractmethod
    def update(self, instance_id, model: BaseModel) -> Project:
        raise NotImplementedError

    @abstractmethod
    def delete(self, instance_id: int) -> None:
        raise NotImplementedError
