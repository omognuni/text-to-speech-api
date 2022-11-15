from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles

from db import engine, SessionLocal
from sqlalchemy.orm import Session

from gtts import gTTS
import os
import re

import models
import config
import schemas
from utils import TextpreProc

REGEX = '[a-zA-z0-9ㄱ-ㅣ가-힣\s!,.?\'\"]+'
SEPERATOR = '[\.\!\?]+'

app = FastAPI()

app.mount("/static/static", StaticFiles(directory=config.STATIC_ROOT), name='static')
app.mount("/static/media", StaticFiles(directory=config.MEDIA_ROOT), name='media')

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        

@app.get("/project")
async def get_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()

@app.get("/project/{project_id}")
async def get_project_detail(project_id:int, db: Session = Depends(get_db)):
    return db.query(models.Project).filter(models.Project.id == project_id).first()


@app.post("/project")
async def create_project(project: schemas.Project, db: Session = Depends(get_db)):
    db_project = models.Project(title=project.title)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.get("/audio")
async def get_audios(db: Session = Depends(get_db)):
    return db.query(models.Audio).all()

@app.get("/audio/{audio_id}", response_model=schemas.AudioDetail)
async def get_audio_detail(audio_id:int, db: Session = Depends(get_db)):
    db_audio = db.query(models.Audio).filter(models.Audio.id == audio_id).join(models.AudioText).first()
    return db_audio

@app.post("/audio")
async def create_audio(audio: schemas.Audio, db: Session = Depends(get_db)):    
    db_audio = models.Audio()
    db_audio.speed = audio.speed
    db_audio.project_id = audio.project_id
    db.add(db_audio)
    db.commit()
    db.refresh(db_audio)
   
    text_pre_proc = TextpreProc(REGEX, SEPERATOR)
    
    texts = text_pre_proc.process(audio.text)
    for text in texts:
        db_audio_text = models.AudioText()
        db_audio_text.index = text[0]
        db_audio_text.content = text[1]
        db_audio_text.audio_id = db_audio.id
        
        new_text = re.sub("[0-9.,?!\s]","",text[1])
        lang = 'ko'
        if new_text.encode().isalpha():
            lang='en'
        
        tts = gTTS(
            text=text[1],
            lang=lang,
        )
        
        folder = os.path.join(config.MEDIA_ROOT, f'{db_audio.id}')
        if not os.path.exists(folder):
            os.mkdir(folder)
        tts.save(os.path.join(folder, f'{text[0]}.mp3'))
        db.add(db_audio_text)
        db.commit()
        db.refresh(db_audio_text)
        
    return db_audio
    
@app.put("/audio/{audio_id}", response_model=schemas.AudioDetail)
async def update_audio(audio_id: int, audio_text: schemas.AudioText, db: Session = Depends(get_db)):
    db_texts = db.query(models.AudioText).filter(models.audio_id == audio_id).all()
    folder = os.path.join(config.MEDIA_ROOT, f'{audio_id}')
    if audio_text:
        for i in range(audio_id, len(db_texts)):
            file = os.path.join(folder, f'{db_texts[i].index}.mp3')
            db_texts[i].index += 1
            db.add(db_texts[i])
            db.commit()
            db.refresh(db_texts[i])
            os.rename(file, '{db_texts[i].index}.mp3')
            
    db_audio_text = models.AudioText(index=audio_text.index, content=audio_text.content, audio_id=audio_id)

    
    db_audio = db.query(models.Audio).filter(models.Audio.id == audio_id).join(models.AudioText).first()
    return  db_audio