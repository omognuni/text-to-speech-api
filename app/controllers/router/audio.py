from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
from dependency_injector.wiring import inject, Provide

import os

from app.controllers.schemas.audio import AudioSchema, AudioDetailSchema
from app.controllers.schemas.project import ProjectSchema
from app.controllers.schemas.text import TextSchema
from app.applications.services.audio import AudioService
from app.applications.services.project import ProjectService
from app.applications.services.text import TextService
from app.infrastructures.containers import AudioContainer
from app.infrastructures.database.exceptions import NotFoundError
from app.controllers.utils import TextpreProc

REGEX = '[a-zA-z0-9ㄱ-ㅣ가-힣\s!,.?\'\"]+'
SEPERATOR = '[\.\!\?]+'

text_pre_proc = TextpreProc(REGEX, SEPERATOR)

router = APIRouter(
    prefix="/audios",
    tags=["audio"],
)


@router.get("/")
@inject
async def get_audios(audio_service: AudioService = Depends(Provide[AudioContainer.audio_service])):
    return audio_service.get_objects()


@router.get("/{audio_id}", response_model=AudioDetailSchema)
@inject
async def get_audio_detail(audio_id: int, audio_service: AudioService = Depends(Provide[AudioContainer.audio_service])):
    audio = audio_service.get_object_by_id(audio_id)
    return audio


@router.get("/{audio_id}/media")
@inject
async def get_audio_file(audio_id: int, audio_service: AudioService = Depends(Provide[AudioContainer.audio_service])):
    file = audio_service.get_media(audio_id)
    return FileResponse(file, media_type='application/octet-stream', filename=f'{audio_id}.zip', background=BackgroundTask(os.remove, file))


@router.post("/")
@inject
async def create(audio: AudioSchema,
                 audio_service: AudioService = Depends(
                     Provide[AudioContainer.audio_service]),
                 text_service: TextService = Depends(
                     Provide[AudioContainer.text_service]),
                 project_service: ProjectService = Depends(
                     Provide[AudioContainer.project_service])
                 ):

    audio = audio.dict()
    project_id = audio.pop('project_id')
    texts = audio.pop('text')

    project_service.get_or_create(id=project_id)
    audio = audio_service.create(project_id=project_id, speed=audio.speed)

    texts = text_pre_proc.process(texts)
    for text in texts:
        text_service.create(audio_id=audio.id, index=text[0], content=text[1])

    return audio


@router.post("/{audio_id}/modify")
@inject
async def modify_audio_text(audio_id: int, audio_text: TextSchema,
                            text_service: TextService = Depends(
                                Provide[AudioContainer.text_service])
                            ):

    content = text_pre_proc.process(audio_text.content)
    try:
        texts = text_service.update(index=audio_text.index,
                                    content=content, audio_id=audio_id
                                    )
        return texts
    except NotFoundError:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/{audio_id}/add")
@inject
async def add_audio_text(audio_id: int, audio_text: TextSchema,
                         text_service: TextService = Depends(
                             Provide[AudioContainer.text_service])
                         ):
    content = text_pre_proc.process(audio_text.content)
    try:
        texts = text_service.insert(
            content=content, audio_id=audio_id, index=audio_text.index)
        return texts

    except NotFoundError:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)


@router.delete("/{audio_id}")
@inject
async def delete_audio(audio_id: int, audio_service: AudioService = Depends(
    Provide[AudioContainer.audio_service])
):
    try:
        audio_service.delete(audio_id)
        return
    except NotFoundError:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
