from typing import Callable, ContextManager
from sqlalchemy.orm import Session

from gtts import gTTS

import os
import shutil
import re

class BaseRepository:
    
    def __init__(self, model, session_factory: Callable[..., ContextManager[Session]]) -> None:
        self.model = model
        self.session_factory = session_factory
        
    def get_all(self):
        with self.session_factory() as session:
            return session.query(self.model).all()
    
    def get_or_create(self, **kwargs):
        with self.session_factory() as session:
            instance = session.query(self.model).filter_by(**kwargs).first()
            if instance:
                return instance
            else:
                instance = self.model(**kwargs)
                session.add(instance)
                session.commit()
                session.refresh(instance)
            return instance
        
    def get_by_id(self, instance_id: int):
        with self.session_factory() as session:
            instance = session.query(self.model).filter(self.model.id == instance_id).first()
            if not instance:
                raise NotFoundError(instance_id)
            return instance
        
    def add(self, **kwargs):
        with self.session_factory() as session:
            instance = self.model(**kwargs)
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return instance
        
    def update(self, instance_id, **kwargs):
        with self.session_factory() as session:
            instance = session.query(self.model).filter(self.model.id == instance_id).first()
            for k, v in kwargs.items():
                setattr(instance, k, v)
            return instance
            
    def delete(self, instance_id: int):
        with self.session_factory() as session:
            instance = session.query(self.model).filter(self.model.id == instance_id).first()
            if not instance:
                raise NotFoundError(instance_id)
            session.delete(instance)
            session.commit()
    
class ProjectRepository(BaseRepository):
    pass

class AudioRepository(BaseRepository):
    pass


class AudioTextRepository(BaseRepository):
    
    def __init__(self, model, session_factory, media_root):
        super().__init__(model, session_factory)
        self.media_root = media_root

    def _folder(self, audio_id):
        return os.path.join(self.media_root, f'{audio_id}')
    
    def _save_tts(self, index, text, audio_id):
        '''text to speech'''
        new_text = re.sub("[0-9.,?!\s]","",text)
        lang = 'ko'
        if new_text.encode().isalpha():
            lang='en'
        tts = gTTS(
            text=text,
            lang=lang,
        )
        
        folder = self._folder(audio_id)
        
        if not os.path.exists(folder):
            os.mkdir(folder)
        tts.save(os.path.join(folder, f'{index}.mp3'))
        return

    def add(self, content: list, audio_id: int, index: int = 0):
        with self.session_factory() as session:
            N = len(content)
            for i in range(N):
                audio_text = self.model(index=index + content[i][0], content=content[i][1], audio_id=audio_id)
                
                session.add(audio_text)
                session.commit()
                session.refresh(audio_text)
                
                self._save_tts(audio_text.index, audio_text.content, audio_id)
                
        return

    def update(self, index, content, audio_id):
        with self.session_factory() as session:
            text = session.query(self.model).filter(self.model.audio_id==audio_id).filter(self.model.index==index).first()
            text.content = content
            session.commit()
            session.refresh(text)
        return
    
    def insert(self, index: int, content: list, audio_id: int):
        with self.session_factory() as session:
            texts = session.query(self.model).filter(self.model.audio_id==audio_id).all()
            N = len(content)
            for i in range(len(texts), index, -1):    
                file = os.path.join(self._folder(audio_id), '{texts[i].index}.mp3')
                texts[i].index += N
                
                session.add(texts[i])
                session.commit()
                session.refresh(texts[i])
                
                os.rename(file, os.path.join(self._folder(audio_id), f'{texts[i].index}.mp3'))
            
            self.add(content=content, audio_id=audio_id, index=index)   
        return
    
    def delete(self, index, audio_id):
        with self.session_factory() as session:
            text = session.query(self.model).filter(self.model.audio_id==audio_id).filter(self.model.index==index).first()
            session.delete(text)
            session.commit()
            
        return


class NotFoundError(Exception):
    
    def __init__(self, entity_id):
        super().__init__(f"not found, id: {entity_id}")