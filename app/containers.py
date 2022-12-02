from dependency_injector import containers, providers

from fastapi.staticfiles import StaticFiles

from database import Database

from infrastructures.repositories import ProjectRepository, AudioRepository, AudioTextRepository
from applications.audio_service import AudioService, ProjectService, AudioTextService
from domains.entities.audio import AudioProject, Audio, AudioText

class AudioContainer(containers.DeclarativeContainer):
              
    db = providers.Dependency()
    
    config = providers.Configuration()
    
    project_repository = providers.Factory(
        ProjectRepository,
        model = AudioProject,
        session_factory = db.provided.session,   
    )
    
    audio_repository = providers.Factory(
        AudioRepository,
        model = Audio,
        session_factory = db.provided.session,       
    )
    
    audio_text_repository = providers.Factory(
        AudioTextRepository,
        model = AudioText,
        session_factory = db.provided.session,
        media_root = config.media_root
    )
    
    audio_service = providers.Factory(
        AudioService,
        repository=audio_repository,
    )
    
    audio_text_service = providers.Factory(
        AudioTextService,
        repository=audio_text_repository
    )
    
    project_service = providers.Factory(
        ProjectService,
        repository=project_repository
    )

class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    
    static = providers.Singleton(StaticFiles, directory=config.static_root)
    media = providers.Singleton(StaticFiles, directory=config.media_root)
    
    db = providers.Singleton(Database, db_url=config.db.url)
    
    audio_package = providers.Container(
        AudioContainer,
        db = db,
        config = config
    )