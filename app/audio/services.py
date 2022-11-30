from typing import Iterator

from audio.repositories import ProjectRepository, AudioRepository, AudioTextRepository
from audio.models import Audio

class AudioService:
    
    def __init__(self, audio_repository: AudioRepository) -> None:
        self._repository: AudioRepository = audio_repository
        
    def get_audios(self) -> Iterator[Audio]:
        return self._repository.get_all()
    
    def get_audio_by_id(self, audio_id: int) -> Audio:
        return self._repository.get_by_id(audio_id)
    
    def create_audio(self, project_id, **kwargs) -> Audio:
        project_id = ProjectRepository.get_or_create(project_id)
        return self._repository.add(project_id, **kwargs)
    
    