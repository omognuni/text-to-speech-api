from dependency_injector import containers, providers

from fastapi.staticfiles import StaticFiles

from app.infrastructures.database.main import Database
from app.infrastructures.database.repository.audio import AudioRepositoryImpl
from app.infrastructures.database.repository.project import ProjectRepositoryImpl
from app.infrastructures.database.repository.text import TextRepositoryImpl

from app.applications.services.audio import AudioService
from app.applications.services.project import ProjectService
from app.applications.services.text import TextService


class AudioContainer(containers.DeclarativeContainer):

    db = providers.Dependency()

    config = providers.Configuration()

    project_repository = providers.Factory(
        ProjectRepositoryImpl,
        session_factory=db.provided.session
    )

    audio_repository = providers.Factory(
        AudioRepositoryImpl,
        session_factory=db.provided.session,
    )

    text_repository = providers.Factory(
        TextRepositoryImpl,
        session_factory=db.provided.session,
    )

    audio_service = providers.Factory(
        AudioService,
        repository=audio_repository,
    )

    text_service = providers.Factory(
        TextService,
        repository=text_repository
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
        db=db,
        config=config
    )
