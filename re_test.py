import re

regex = '[a-zA-z0-9ㄱ-ㅣ가-힣\s!,.?\'\"]+'
sep = '[\.\!\?]+'
s = re.compile(regex)

text="입력 \'tex##$t\' list는 @)()\"길이\"@@@가 1입니다@@!!! 빈 문장은 삭제됩니다. 한글, 영어, 숫자, 물음표, 느낌표, 마침표, 따옴표, 공백을 제외한 나머지는 문장에  포함되지 않습니다. 문장의 맨앞, 맨뒤에는 공백이 위치하지 않습니다."
# text="바꾸기 1"

result = s.findall(text)
# print(''.join(result))


class TextpreProc:
    
    def __init__(self, regex: str, sep: str):
        self.regex = re.compile(regex)
        self.sep = re.compile(sep)
               
    def _split_result(self, result: str):
        separtors = self.sep.finditer(result)
        splited_result = []
        start = 0
        for sep in separtors:
            splited_result.append(result[start:sep.end()+1])
            start = sep.end() + 1
        return splited_result
    
    def _sort_result(self, result: list) -> list:
        for i in range(len(result)):
            result[i] = [i] + [result[i].strip()]
        return result
    
    def filter_text(self, text: str):
        return self.regex.findall(text)
    
    def process(self, text: str):
        result = self.filter_text(text)
        result = ''.join(result)
        splited_result = self._split_result(result)
        sorted_result = self._sort_result(splited_result)
        if not splited_result:
            sorted_result = self._sort_result([result])
        return sorted_result
        

text_preproc = TextpreProc(regex, sep)

print(text_preproc.process(text))
