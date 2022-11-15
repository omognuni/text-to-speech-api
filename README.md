#
```
docker-compose exec tts pytest .
```
- ['입력 텍스트 리스트는 길이가 1 입니다. 구분은 점, 느낌표, 물음표로 구분됩니다.']
- 전처리 후
- ['입력 텍스트 리스트는 길이가 1 입니다.', '구분은 점, 느낌표, 물음표로 구분됩니다.'], path

- '.', '!', '?' 로 split()
- 빈 문장 삭제
- 한글, 영어, 숫자, 물음표, 느낌표, 마침표, 따옴표, 공백 제외 나머지는 문장 포함 x,
- re.compile('[a-zA-z0-9ㄱ-ㅣ가-힣]')


- post api/v1/audio

- api/v1/audio/audio_id/text
- 텍스트 조회 METHOD GET
- 텍스트 생성, 중간 삽입 METHOD POST payload {text:[]}, query_params {index:}
- 텍스트 삭제 METHOD DELETE query_params {index:}