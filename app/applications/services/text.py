from app.applications.interfaces.text_repository import TextRepository
from app.domains.entities import Text


class TextService:

    def __init__(self, repository: TextRepository) -> None:
        self._repository = repository

    def get_objects(self):
        return self._repository.get_all()

    def create(self, text: Text):
        return self._repository.add(text)

    def update(self, content: list, audio_id: int, index: int):
        return self._repository.update(content, audio_id, index)

    def delete(self, object_id):
        return self._repository.delete(object_id)

    def insert(self, content: list, audio_id: int, index: int):
        return self._repository.insert(content, audio_id, index)
