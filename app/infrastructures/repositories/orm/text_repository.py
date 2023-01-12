from typing import Callable, ContextManager, Tuple
from sqlalchemy.orm import Session

from infrastructures.exceptions import NotFoundError
from infrastructures.repositories.repository import AbstractRepository


class AudioTextRepository(AbstractRepository):


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