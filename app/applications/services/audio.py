from app.applications.interfaces.audio_repository import AudioRepository
from app.domains.entities.audio import Audio


class AudioService:

    def __init__(self, repository: AudioRepository) -> None:
        self._repository = repository

    def get_objects(self):
        return self._repository.get_all()

    def get_object_by_id(self, audio: Audio):
        return self._repository.get_by_id(audio.id)

    def create(self, audio: Audio):
        return self._repository.add(audio)

    def get_or_create(self, audio: Audio):
        return self._repository.get_or_create(audio)

    def update(self, audio: Audio):
        return self._repository.update(audio)

    def delete(self, audio: Audio):
        return self._repository.delete(audio.id)
