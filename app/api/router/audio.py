from fastapi import APIRouter, Depends, Response, status
from dependency_injector.wiring import inject, Provide

from gtts import gTTS
import os
import shutil
import re

from schemas.audio import AudioSchema, AudioDetailSchema, AudioTextSchema
from schemas.project import ProjectSchema
from containers import AudioContainer
from applications.audio_service import AudioService, AudioTextService, ProjectService
from api.utils import TextpreProc


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


@router.post("/")
@inject
async def create(audio: AudioSchema,
           audio_service: AudioService = Depends(
               Provide[AudioContainer.audio_service]),
           audio_text_service: AudioTextService = Depends(
               Provide[AudioContainer.audio_text_service]),
           project_service: ProjectService = Depends(
               Provide[AudioContainer.project_service])
           ):

    audio_dict = audio.dict()
    project_id = audio_dict.pop('project_id')
    texts = audio_dict.pop('text')

    project_service.get_or_create(id=project_id)
    audio = audio_service.create(project_id=project_id, **audio_dict)

    texts = text_pre_proc.process(texts)
    audio_text_service.create(audio_id=audio.id, content=texts)

    return


@router.post("/{audio_id}/modify")
@inject
async def modify_audio_text(audio_id: int, audio_text: AudioTextSchema,
                            audio_text_service: AudioTextService = Depends(
                                Provide[AudioContainer.audio_text_service])
                            ):
    
    content = text_pre_proc.process(audio_text.content)
    audio_text_service.update(index=audio_text.index,
                              content=content, audio_id=audio_id
                              )
    return

@router.post("/{audio_id}/add")
@inject
async def add_audio_text(audio_id: int, audio_text: AudioTextSchema,
                            audio_text_service: AudioTextService = Depends(
                                Provide[AudioContainer.audio_text_service])
                            ):
    content = text_pre_proc.process(audio_text.content)
    audio_text_service.create(content=content, audio_id=audio_id, index=audio_text.index)
    
    return
    

@router.delete("/{audio_id}")
@inject
async def delete_audio(audio_id: int, audio_service: AudioService = Depends(
                                Provide[AudioContainer.audio_service])
                       ):
    
    audio_service.delete(audio_id)
    return
