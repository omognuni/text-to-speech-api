from app.applications.interfaces.text_repository import TextRepository


class TextService:

    def __init__(self, repository: TextRepository) -> None:
        self._repository = repository

    def get_objects(self):
        return self._repository.get_all()

    def create(self, **kwargs):
        return self._repository.add(**kwargs)

    def update(self, **kwargs):
        return self._repository.update(**kwargs)

    def delete(self, object_id):
        return self._repository.delete(object_id)
