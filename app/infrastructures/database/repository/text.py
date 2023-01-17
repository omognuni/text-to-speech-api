from typing import Callable, ContextManager, Tuple, List
from sqlalchemy.orm import Session

from app.applications.interfaces.text_repository import TextRepository
from app.domains.entities import Text
from app.infrastructures.database.exceptions import NotFoundError


class TextRepositoryImpl(TextRepository):
    def __init__(self, session_factory: Callable[..., ContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self) -> List[Text]:
        with self.session_factory() as session:
            return session.query(Text).all()
        ...

    def add(self, content: list, audio_id: int, index: int = 0):
        with self.session_factory() as session:
            N = len(content)
            for i in range(N):
                audio_text = Text(
                    index=index + content[i][0], content=content[i][1], audio_id=audio_id)

                session.add(audio_text)
                session.commit()
                session.refresh(audio_text)

                self._save_tts(audio_text.index, audio_text.content, audio_id)
            texts = session.query(Text).filter(
                Text.audio_id == audio_id).order_by(Text.index).all()
            return texts

    def update(self, index: int, content: list[str], audio_id: int):
        with self.session_factory() as session:
            text = session.query(Text).filter(
                Text.audio_id == audio_id).filter(Text.index == index).first()
            if not text:
                raise NotFoundError(index)
            update = content.pop(0)
            text.content = update[1]
            session.commit()
            session.refresh(text)

            for i in range(len(content)):
                content[i][0] -= 1
        texts = self.insert(index=index+1, content=content, audio_id=audio_id)
        return texts

    def insert(self, index: int, content: list, audio_id: int):
        with self.session_factory() as session:
            texts = session.query(Text).filter(
                Text.audio_id == audio_id).order_by(Text.index).all()
            N = len(content)
            for i in range(len(texts)-1, index - 1, -1):
                texts[i].index += N

                session.add(texts[i])
                session.commit()
                session.refresh(texts[i])
        texts = self.add(content=content, audio_id=audio_id, index=index)
        return texts

    def delete(self, index, audio_id):
        with self.session_factory() as session:
            texts = session.query(Text).filter(
                audio_id == audio_id).all()

            text = session.query(Text).filter(
                Text.audio_id == audio_id).filter(Text.index == index).first()
            if not text:
                raise NotFoundError(index)

            session.delete(text)
            session.commit()

            for i in range(index+1, len(texts)):
                texts[i].index = texts[i].index - 1

                session.add(texts[i])
                session.commit()
                session.refresh()
