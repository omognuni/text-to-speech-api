from typing import Callable, ContextManager
from sqlalchemy.orm import Session

from gtts import gTTS

import os
import shutil
import re
# import zipfile

from domains.entities.audio import Audio, AudioText

class BaseRepository:

    def __init__(self, model, session_factory: Callable[..., ContextManager[Session]], media_root: str = '') -> None:
        self.model = model
        self.session_factory = session_factory
        self.media_root = media_root

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
            instance = session.query(self.model).filter(
                self.model.id == instance_id).first()
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
            instance = session.query(self.model).filter(
                self.model.id == instance_id).first()
            for k, v in kwargs.items():
                setattr(instance, k, v)
            return instance

    def delete(self, instance_id: int):
        with self.session_factory() as session:
            instance = session.query(self.model).filter(
                self.model.id == instance_id).first()
            if not instance:
                raise NotFoundError(instance_id)
            session.delete(instance)
            session.commit()


class ProjectRepository(BaseRepository):

    def _folder(self, audio_id):
        return os.path.join(self.media_root, f'{audio_id}')

    def get_by_id(self, project_id: int):
        with self.session_factory() as session:
            instance = session.query(self.model).filter(
                self.model.id == project_id).first()
            if not instance:
                raise NotFoundError(project_id)
            return instance

    def delete(self, project_id: int):
        with self.session_factory() as session:
            project = session.query(self.model).filter(
                self.model.id == project_id).first()
            if not project:
                raise NotFoundError(project_id)
            session.delete(project)
            session.commit()

            for audio in project.audios:
                try:
                    shutil.rmtree(os.path.join(self._folder(audio.id)))
                except FileNotFoundError:
                    pass
        return


class AudioRepository(BaseRepository):

    def _folder(self, audio_id):
        return os.path.join(self.media_root, f'{audio_id}')

    def get_by_id(self, audio_id: int):
        with self.session_factory() as session:
            instance = session.query(self.model).filter(
                self.model.id == audio_id).join(AudioText).first()
            if not instance:
                raise NotFoundError(audio_id)
            return instance

    def delete(self, audio_id: int):
        with self.session_factory() as session:
            audio = session.query(self.model).filter(
                self.model.id == audio_id).first()
            if not audio:
                raise NotFoundError(audio_id)
            session.delete(audio)
            session.commit()
            shutil.rmtree(os.path.join(self._folder(audio_id)))
        return

    def get_media(self, audio_id: int):
        try:
            path = shutil.make_archive(self._folder(audio_id), 'zip', self._folder(audio_id) )
            return path
        except FileNotFoundError:
            return

class AudioTextRepository(BaseRepository):

    def _folder(self, audio_id):
        return os.path.join(self.media_root, f'{audio_id}')

    def _save_tts(self, index, text, audio_id):
        '''text to speech'''
        new_text = re.sub("[0-9.,?!\s]", "", text)
        lang = 'ko'
        if new_text.encode().isalpha():
            lang = 'en'
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
                audio_text = self.model(
                    index=index + content[i][0], content=content[i][1], audio_id=audio_id)

                session.add(audio_text)
                session.commit()
                session.refresh(audio_text)

                self._save_tts(audio_text.index, audio_text.content, audio_id)
            texts = session.query(self.model).filter(self.model.audio_id == audio_id).order_by(self.model.index).all()
            return texts

    def update(self, index: int, content: list[str], audio_id: int):
        with self.session_factory() as session:
            text = session.query(self.model).filter(
                self.model.audio_id == audio_id).filter(self.model.index == index).first()
            if not text:
                    raise NotFoundError(index)
            update = content.pop(0)
            text.content = update[1]
            session.commit()
            session.refresh(text)
            self._save_tts(index=index, text=update[1], audio_id=audio_id)
            for i in range(len(content)):
                content[i][0] -= 1
        texts = self.insert(index=index+1, content=content, audio_id=audio_id)
        return texts

    def insert(self, index: int, content: list, audio_id: int):
        with self.session_factory() as session:
            texts = session.query(self.model).filter(
                self.model.audio_id == audio_id).order_by(self.model.index).all()
            N = len(content)
            for i in range(len(texts)-1, index - 1, -1):
                file = os.path.join(self._folder(audio_id),
                                    f'{texts[i].index}.mp3')
                texts[i].index += N

                session.add(texts[i])
                session.commit()
                session.refresh(texts[i])

                os.rename(file, os.path.join(self._folder(
                    audio_id), f'{texts[i].index}.mp3'))

        texts = self.add(content=content, audio_id=audio_id, index=index)
        return texts

    def delete(self, index, audio_id):
        with self.session_factory() as session:
            texts = session.query(self.model).filter(
                audio_id == audio_id).all()

            text = session.query(self.model).filter(
                self.model.audio_id == audio_id).filter(self.model.index == index).first()
            if not text:
                raise NotFoundError(index)

            session.delete(text)
            session.commit()
            os.remove(os.path.join(self._folder(audio_id), f'{index}.mp3'))

            for i in range(index+1, len(texts)):
                file = os.path.join(self._folder(audio_id),
                                    f'{texts[i].index}.mp3')
                texts[i].index = texts[i].index - 1

                session.add(texts[i])
                session.commit()
                session.refresh()

                os.rename(file, os.path.join(self._folder(
                    audio_id), f'{texts[i].index}.mp3'))

        return


class NotFoundError(Exception):

    def __init__(self, entity_id):
        super().__init__(f"not found, id: {entity_id}")
