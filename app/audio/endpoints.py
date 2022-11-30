from fastapi import APIRouter, Depends, Response, status
from dependency_injector.wiring import inject, Provide

from audio.containers import Container
from audio.services import AudioService
from audio.repositories import NotFoundError

router = APIRouter(
    prefix="/audios",
    tags=["audio"],
)
@router.get("/")
@inject
def get_audios(audio_service: AudioService = Depends(Provide[Container.audio_service])):
    return audio_service.get_audios()