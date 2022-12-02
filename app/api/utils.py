import re

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