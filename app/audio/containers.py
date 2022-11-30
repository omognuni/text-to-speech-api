from dependency_injector import containers, providers

from containers import ApplicationContainer
from audio.repositories import ProjectRepository, AudioRepository
from audio.services import AudioService
from audio.models import Project, Audio, AudioText


class AudioContainer(containers.DeclarativeContainer):
    
    wiring_config = containers.WiringConfiguration(modules=[".endpoints"])
    
    db = providers.Dependency()
    
    project_repository = providers.Factory(
        ProjectRepository,
        model = Project,
        session_factory = db.provided.session,   
    )
    
    audio_repository = providers.Factory(
        AudioRepository,
        model = Audio,
        session_factory = db.provided.session,       
    )
    
    audio_text_repository = providers.Factory(
        
    )
    
    audio_service = providers.Factory(
        AudioService,
        audio_repository=audio_repository,
    )