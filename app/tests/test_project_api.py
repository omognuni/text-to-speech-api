from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)



def test_create_project():
    pass

def test_create_audio():
    pass

def test_get_audio_text():
    pass

def test_add_audio_text():
    pass

def test_insert_audio_between_texts():
    pass

def test_delete_audio_text():
    pass