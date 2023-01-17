
from app.applications.interfaces.project_repository import ProjectRepository

from app.domains.entities.project import Project


class ProjectService:
    def __init__(self, repository: ProjectRepository) -> None:
        self._repository = repository

    def get_objects(self):
        return self._repository.get_all()

    def get_object_by_id(self, project: Project):
        return self._repository.get_by_id(project.id)

    def create(self, **kwargs):
        return self._repository.add(**kwargs)

    def get_or_create(self, **kwargs):
        return self._repository.get_or_create(**kwargs)

    def update(self, **kwargs):
        return self._repository.update(**kwargs)

    def delete(self, object_id):
        return self._repository.delete(object_id)
