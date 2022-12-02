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

text_pre_proc = TextpreProc(REGEX,SEPERATOR)

router = APIRouter(
    prefix="/audios",
    tags=["audio"],
)

@router.get("/")
@inject
def get_audios(audio_service: AudioService = Depends(Provide[AudioContainer.audio_service])):
    return audio_service.get_objects()

@router.post("/")
@inject
def create(audio: AudioSchema, 
           audio_service: AudioService = Depends(Provide[AudioContainer.audio_service]),
           audio_text_service: AudioTextService = Depends(Provide[AudioContainer.audio_text_service]),
           project_service: ProjectService = Depends(Provide[AudioContainer.project_service])
           ):
    audio_dict = audio.dict()
    project_id = audio_dict.pop('project_id')
    texts = audio_dict.pop('text')
    
    project_service.get_or_create(id=project_id)
    audio = audio_service.create(project_id = project_id, **audio_dict)

    texts = text_pre_proc.process(texts)
    
    audio_text_service.create(audio_id=audio.id, content=texts)
    return