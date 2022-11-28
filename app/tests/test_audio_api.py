import pytest
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app.main import app


def test_create_audio(client: TestClient, session: Session):
    payload = {
        'speed': 1,
        'text': '입력 tex##$t list는 @)()길이@@@가 1입니다@@!!!\
            빈 문장은 삭제됩니다. \
            한글, 영어, 숫자, 물음표, 느낌표, 마침표, 따옴표, 공백을 제외한 나머지는 문장에 포함되지 않습니다.\
            문장의 맨앞, 맨뒤에는 공백이 위치하지 않습니다.',
        'project_id': 1
    }
    
    answer = ['입력 text list는 길이가 1입니다!!!', '빈 문장은 삭제됩니다.', \
        '한글, 영어, 숫자, 물음표, 느낌표, 마침표, 따옴표, 공백을 제외한 나머지는 문장에 포함되지 않습니다.', \
            '문장의 맨앞, 맨뒤에는 공백이 위치하지 않습니다.']
    
    url = app.url_path_for('create_audio')
    res = client.post(url, json=payload)
    texts = res.json()['texts']

    assert len(texts) == 4
    for i in range(len(texts)):
        assert texts[i]['content'] == answer[i]
    assert res.status_code == 201
    
def test_get_audios(client: TestClient, session: Session):
    res = client.get(app.url_path_for('get_audios'))

    assert len(res.json()) == 1
    assert res.status_code == 200
    
# @pytest.fixture(scope='function')
# def test_add_audio_text():
#     pass

# @pytest.fixture(scope='function')
# def test_insert_audio_between_texts():
#     pass

# @pytest.fixture(scope='function')
# def test_delete_audio_text():
#     pass