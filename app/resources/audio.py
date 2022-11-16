from fastapi import APIRouter, Depends, HTTPException

from db import engine, SessionLocal
from sqlalchemy.orm import Session

from gtts import gTTS
import os
import shutil
import re

import db
import config
from schemas import audio as schemas
from models import audio as models
from utils.text import TextpreProc

REGEX = '[a-zA-z0-9ㄱ-ㅣ가-힣\s!,.?\'\"]+'
SEPERATOR = '[\.\!\?]+'

router = APIRouter(
    prefix="/audio",
    tags=["audio"],
)

text_pre_proc = TextpreProc(REGEX, SEPERATOR)

db.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        

async def save_tts(index, text, audio_id):
    '''text to speech'''
    new_text = re.sub("[0-9.,?!\s]","",text)
    lang = 'ko'
    if new_text.encode().isalpha():
        lang='en'
    tts = gTTS(
        text=text,
        lang=lang,
    )
    
    folder = os.path.join(config.MEDIA_ROOT, f'{audio_id}')
    
    if not os.path.exists(folder):
        os.mkdir(folder)
    tts.save(os.path.join(folder, f'{index}.mp3'))
    return


@router.get("/")
async def get_audios(db: Session = Depends(get_db)):
    return db.query(models.Audio).all()

@router.get("/{audio_id}", response_model=schemas.AudioDetail)
async def get_audio_detail(audio_id:int, db: Session = Depends(get_db)):
    db_audio = db.query(models.Audio).filter(models.Audio.id == audio_id).join(models.AudioText).first()
    if db_audio is None:
        raise HTTPException(status_code=404, detail='Audio not found')
    return db_audio

@router.post("/")
async def create_audio(audio: schemas.Audio, db: Session = Depends(get_db)):    
    db_audio = models.Audio()
    db_audio.speed = audio.speed
    db_audio.project_id = audio.project_id
    db.add(db_audio)
    db.commit()
    db.refresh(db_audio)
    
    texts = text_pre_proc.process(audio.text)
    for text in texts:
        db_audio_text = models.AudioText()
        db_audio_text.index = text[0]
        db_audio_text.content = text[1]
        db_audio_text.audio_id = db_audio.id
        
        await save_tts(text[0], text[1], db_audio.id)

        db.add(db_audio_text)
        db.commit()
        db.refresh(db_audio_text)
        
    return db_audio


@router.post("/{audio_id}/modify")
async def modify_audio_text(audio_id: int, audio_text: schemas.AudioText, db: Session = Depends(get_db)):
    db_text = db.query(models.AudioText).filter(models.AudioText.audio_id == audio_id).filter(models.AudioText.index == audio_text.index).first()
    if db_text is None:
        raise HTTPException(status_code=404, detail='Text not found')
    texts = text_pre_proc.process(audio_text.content)
    if len(texts) > 1:
        return ValueError
    db_text.content = texts[0][1]
    db.add(db_text)
    db.commit()
    db.refresh(db_text)
    await save_tts(db_text.index, texts[0][1], audio_id)
    
    return {'status': 200}

@router.post("/{audio_id}/remove")
async def delete_audio_text(audio_id: int, index: int, db: Session = Depends(get_db)):
    db_text = db.query(models.AudioText).filter(models.AudioText.audio_id == audio_id).filter(models.AudioText.index == index)
    if db_text is None:
        raise HTTPException(status_code=404, detail='Text not found')
    
    await os.remove(os.path.join(config.MEDIA_ROOT, f'{audio_id}', f'{index}.mp3'))
    db_texts = db.query(models.AudioText).filter(models.AudioText.audio_id == audio_id).all()
    for i in range(index+1, len(db_texts)):
        file = os.path.join(config.MEDIA_ROOT, f'{audio_id}', f'{db_texts[i].index}.mp3')
        db_texts[i].index -= 1
        db.add(db_texts[i])
        db.commit()
        db.refresh(db_texts[i])
        os.rename(file, os.path.join(config.MEDIA_ROOT, f'{audio_id}', f'{db_texts[i].index}.mp3'))
        
    db_text.delete()
    db.commit()
    
    return { 'status': 204 }

@router.post("/{audio_id}/add", response_model=schemas.AudioDetail)
async def add_audio_text(audio_id: int, audio_text: schemas.AudioText, db: Session = Depends(get_db)):
    if db.query(models.Audio).filter(models.Audio.id == audio_id) is None:
        raise HTTPException(status_code=404, detail='Audio not found')
    
    db_texts = db.query(models.AudioText).filter(models.AudioText.audio_id == audio_id).all()
    folder = os.path.join(config.MEDIA_ROOT, f'{audio_id}')
    index = audio_text.index
    texts = audio_text.content
    
    if texts:     
        texts = text_pre_proc.process(texts)
        N = len(texts)
        
        for i in range(len(db_texts), index, -1):
            file = os.path.join(folder, f'{db_texts[i].index}.mp3')
            db_texts[i].index += N
            db.add(db_texts[i])
            db.commit()
            db.refresh(db_texts[i])
            await os.rename(file, os.path.join(folder, f'{db_texts[i].index}.mp3'))
            
        for i in range(N):
            db_audio_text = models.AudioText()
            db_audio_text.index = index + texts[i][0]
            db_audio_text.content = texts[i][1]
            db_audio_text.audio_id = audio_id
            
            await save_tts(index + texts[i][0], texts[i][1], audio_id)
            
            db.add(db_audio_text)
            db.commit()
            db.refresh(db_audio_text)
            
    db_audio = db.query(models.Audio).filter(models.Audio.id == audio_id).join(models.AudioText).first()
    
    return  db_audio

@router.delete('/{audio_id}')
async def delete_audio(audio_id: int, db: Session = Depends(get_db)):
    audio = db.query(models.Audio).filter(models.Audio.id == audio_id).first()
    if audio is None:
        raise HTTPException(status_code=404)
    # db.query(models.Audio).filter(models.Audio.id == audio_id).delete()
    db.delete(audio)
    db.commit()
    shutil.rmtree(os.path.join(config.MEDIA_ROOT, f'{audio_id}'))
    
    return { 'status': 204 }