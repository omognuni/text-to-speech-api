import pytest
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from datetime import datetime
from domains.entities.audio import Audio, AudioText, AudioProject

from fastapi.testclient import TestClient

from main import app


def test_get_audios(client: TestClient, session: Session):
    project = AudioProject(title='test')
    session.add(project)
    session.commit()
    audio_list = [
        {
            "speed": 1,
            "project_id": project.id,
        },
        {
            "speed": 1,
            "project_id": project.id,
        },
        {
            "speed": 1,
            "project_id": project.id,
        }
    ]
    
    audio_text_list = [
        {
            "index": 1,
            "content": "test",
            "audio_id": 1
        },
        {
            "index": 2,
            "content": "test",
            "audio_id": 1
        },
        {
            "index": 1,
            "content": "test",
            "audio_id": 2
        },
        {
            "index": 2,
            "content": "test",
            "audio_id": 2
        }
    ]
    
    audios = list(map(lambda x: Audio(**x), audio_list))
    audio_texts = list(map(lambda x: AudioText(**x), audio_text_list))
    session.add_all(audios)
    session.add_all(audio_texts)
    session.commit()
    
    res = client.get('/api/v1/audios')
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 3
    
def test_get_audio_detail(client: TestClient, session:Session):
    project = AudioProject(title='test')
    session.add(project)
    session.commit()
    audio = Audio(speed=1,project_id=project.id)
    session.add(audio)
    session.commit()
    
    audio_text_list = [
        {
            "index": 1,
            "content": "test",
            "audio_id": audio.id
        },
        {
            "index": 2,
            "content": "test",
            "audio_id": audio.id
        }
    ]
    audio_texts = list(map(lambda x: AudioText(**x), audio_text_list))
    session.add_all(audio_texts)
    session.commit()
    
    res = client.get(f'/api/v1/audios/{audio.id}')
    assert res.status_code == 200
    data = res.json()
    assert data == {
        "speed": 1,
        "project_id": project.id,
        "texts" : [        {
            "index": 1,
            "content": "test"
        },
        {
            "index": 2,
            "content": "test"
        }]
    }