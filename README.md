###  실행
```
docker-compose up --build
```
- localhost:8000/ 으로 접속
- localhost:8000/docs 문서

### ERD

<img src='/images/ERD.png'>

### TODO
- 테스트 코드 작성
- user 생성
- refactor (db.add()/commit()/refresh 반복 없애기)
- ~~파일 구조 변경~~
- ~~url 구조 변경~~

### 설명
- input
- 빈 문장 삭제
- 한글, 영어, 숫자, 물음표, 느낌표, 마침표, 따옴표, 공백 제외 나머지는 문장 포함 x,

### Project

| 내용              | Method | URL                   |
| ----------------- | ------ | --------------------- |
| 프로젝트 가져오기 | GET    | /project              |
| 프로젝트 생성     | POST   | /project              |
| 프로젝트 상세     | GET    | /project/{project_id} |
| 프로젝트 삭제     | DELETE | /project/{project_id} |

### Audio

| 내용              | Method | URL                      |
| ----------------- | ------ | ------------------------ |
| Audio 가져오기    | GET    | /audio                   |
| Audio 생성        | POST   | /audio                   |
| Audio 상세        | GET    | /audio/{audio_id}        |
| Audio 삭제        | DELETE | /audio/{audio_id}        |
| Audio 텍스트 수정 | POST   | /audio/{audio_id}/modify |
| Audio 텍스트 추가 | POST   | /audio/{audio_id}/add    |
| Audio 텍스트 삭제 | POST   | /audio/{audio_id}/remove |

### 기타 
- fastapi 배우면서 기능구현, docker 설정, 테스트 코드 작성하기는 너무 시간이 부족했다.
- async 기능은 알고는 있었지만 처음 사용하는데, for문 돌면서 파일 만들거나 삭제할때 await 안하면 예상과는 다르게 작동하는 부분이 있었다. 비동기적인 부분을 고려하면서 코드짜야할 듯