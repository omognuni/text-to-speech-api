from typing import List, Tuple

from app.applications.interfaces.audio_repository import AudioRepository
from app.domains.entities import Audio


class AudioService:

    def __init__(self, repository: AudioRepository) -> None:
        self._repository = repository

    def get_objects(self) -> List[Audio]:
        return self._repository.get_all()

    def get_object_by_id(self, audio: Audio) -> Audio:
        return self._repository.get_by_id(audio.id)

    def create(self) -> Audio:
        return self._repository.add()

    def update(self, audio: Audio) -> Audio:
        return self._repository.update(audio)

    def delete(self, audio: Audio) -> None:
        return self._repository.delete(audio.id)
