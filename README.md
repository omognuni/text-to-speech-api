###  실행
```
docker-compose up --build
```
- localhost:8000/ 으로 접속
- localhost:8000/docs 문서

### ERD

<img src='/images/ERD.png'>

### TODO
- Clean architecture 적용
  - 적용 전 버전
- Test code 작성

### 설명
1. Project 생성
2. Audio 생성
   - input

    ```
    {   
        "speed": 오디오의 스피드
        "text": 오디오로 변환될 텍스트
        "project_id": 오디오를 포함할프로젝트 id
    }
    ```
   - 텍스트를 받음
   - 이를 전처리하여 오디오 생성
     - 마침표, 느낌표, 물음표로 문장 구분
     - 빈 문장 삭제
     - 한글, 영어, 숫자, 물음표, 느낌표, 마침표, 따옴표, 공백 제외 나머지는 문장 포함 x,
     - 문장의 맨앞, 맨뒤에는 공백 x
   - 전처리 후 text는 [(1, text1), (2, text2), (3, text3)...] 리스트로 리턴되고 각각 AudioText 테이블에 index = 1, text = text1 식으로 저장됨 
   - 생성된 오디오는 /vol/web/static/media에 {audio_id}/{index}.mp3 로 저장됨

3. 텍스트 수정, 삽입, 삭제
   - 생성된 오디오의 텍스트들은 삭제, 수정하거나 중간에 새로운 텍스트를 삽입할 수 있음
  

### Project

| 내용              | Method | URL                         |
| ----------------- | ------ | --------------------------- |
| 프로젝트 가져오기 | GET    | api/v1/project              |
| 프로젝트 생성     | POST   | api/v1/project              |
| 프로젝트 상세     | GET    | api/v1/project/{project_id} |
| 프로젝트 삭제     | DELETE | api/v1/project/{project_id} |

### Audio

| 내용              | Method | URL                            |
| ----------------- | ------ | ------------------------------ |
| Audio 가져오기    | GET    | api/v1/audio                   |
| Audio 생성        | POST   | api/v1/audio                   |
| Audio 상세        | GET    | api/v1/audio/{audio_id}        |
| Audio 삭제        | DELETE | api/v1/audio/{audio_id}        |
| Audio 텍스트 수정 | POST   | api/v1/audio/{audio_id}/modify |
| Audio 텍스트 추가 | POST   | api/v1/audio/{audio_id}/add    |
| Audio 텍스트 삭제 | POST   | api/v1/audio/{audio_id}/remove |
| Audio 다운로드    | POST   | api/v1/audio/{audio_id}/media  |


### 전체 흐름


### 고려사항
- text를 음성 파일로 변환 중에 멈추면(서버 다운) 어떻게 해야하는지 -> is_converted 행을 audio 모델에 추가하여 변환 완료 시에만 True로 설정
- 동시성 제어는 어떻게 할 것인지? (음성 파일 변환 중에 다른 유저에 의해 text가 업데이트 되는 경우)
- media 파일을 저장하는 기능은 어느 layer에 생성해야하는지?
- audio와 text의 1:N 관계에서 N+1 문제는 어떻게 해결할 것인지? -> relationship(... lazy='selectin')