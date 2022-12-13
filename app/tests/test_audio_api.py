from unittest import mock
from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from infrastructures.repositories import AudioRepository, AudioTextRepository
from domains.entities.audio import Audio, AudioText
from main import app

DT_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'


@pytest.fixture
def client():
    yield TestClient(app)
    
    
class TestAudioApi:

    @pytest.fixture(scope="class")
    def audio_repo_mock(self):
        return mock.Mock(spec=AudioRepository)
    
    def test_get_audios(self, client, audio_repo_mock):
        '''오디오 목록 가져오기 테스트'''
        update_time = datetime.now()
        audio_repo_mock.get_all.return_value = [
            Audio(id=1, speed=1, project_id=1, updated_at=update_time),
            Audio(id=2, speed=1, project_id=1, updated_at=update_time)
        ]
        
        with app.container.audio_package.audio_repository.override(audio_repo_mock):
            res = client.get("/api/v1/audios")
            
        assert res.status_code == 200
        data = res.json()
        assert data == [
            {"id": 1, "speed": 1, "project_id": 1, "updated_at": update_time.strftime(DT_FORMAT)},
            {"id": 2, "speed": 1, "project_id": 1, "updated_at": update_time.strftime(DT_FORMAT)}
        ]
        
    def test_get_audio_detail(self, client, audio_repo_mock):
        '''오디오 상세 테스트'''
        audio_repo_mock.get_by_id.return_value = Audio(
            speed=1, project_id=1, texts=[AudioText(index=1, content='테스트입니다.')]
            )

        with app.container.audio_package.audio_repository.override(audio_repo_mock):
            res = client.get("/api/v1/audios/1")
        
        assert res.status_code == 200
        data = res.json()
        assert data == {"speed": 1, "project_id": 1, "texts": [{"index": 1 ,"content":"테스트입니다."}]}
        
    def test_create_audio(self):
        '''오디오 생성 테스트'''
        pass
        
class TestAudioText:
    
    @pytest.fixture(scope="class")
    def audio_text_repo_mock(self):
        return mock.Mock(spec=AudioTextRepository)