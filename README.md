# hangulpy

hangulpy는 한글 처리를 위한 파이썬 라이브러리입니다. es-hangul의 파이썬 버전으로, 초성 검색과 조사 붙이기 등의 기능을 제공합니다.

## 설치

```bash
pip install hangulpy
```

## 사용법

모든 기능은 [위키 문서](https://wiki.uiharu.dev/w/hangulpy)를 확인하세요!

### 초성 검색

```python
from hangulpy import chosungIncludes

searchWord = '라면'
userInput = 'ㄹㅁ'

result = chosungIncludes(searchWord, userInput)
print(result)  # True
```

### 조사 붙이기

```python
from hangulpy import josa

word1 = '사과'
sentence1 = josa(word1, '을/를') + ' 먹었습니다.'
print(sentence1)  # '사과를 먹었습니다.'

word2 = '바나나'
sentence2 = josa(word2, '이/가') + ' 맛있습니다.'
print(sentence2)  # '바나나가 맛있습니다.'
```

### 자음 또는 모음 여부

```python
from hangulpy import is_hangul_consonant, is_hangul_vowel

char1 = 'ㄱ'
char2 = 'ㅏ'

print(is_hangul_consonant('ㄱ'))  # True
print(is_hangul_consonant('ㅏ'))  # False
print(is_hangul_vowel('ㅏ'))  # True
print(is_hangul_vowel('ㄱ'))  # False
```

### 문자열 포함 여부 확인

```python
from hangulpy import hangul_contains

word = '사과'
print(hangul_contains(word, ''))  # True
print(hangul_contains(word, '', notallowempty=True))  # False
print(hangul_contains(word, 'ㅅ'))  # True
print(hangul_contains(word, '삭'))  # True
print(hangul_contains(word, '삽'))  # False
print(hangul_contains(word, '사과'))  # True

# 문장처럼 입력 값 사이에 공백이 포함된 경우
print(hangul_contains('사과는 맛있다', '사과는 ㅁ'))  # True
print(hangul_contains('사과는 맛있다', '사과는 '))  # True
```

### 초/중/종성 분해(문자열 변환)
```python
from hangulpy import decompose_hangul_char

char = '괜'
print(decompose_hangul_char(char))  # ('ㄱ', ('ㅗ', 'ㅐ'), ('ㄴ', 'ㅈ'))
```

#### 분해 시 배열로 반환
```python
char1 = '값'
print(split_hangul_char(char1))  # ['ㄱ', 'ㅏ', 'ㅂ', 'ㅅ']

char2 = 'ㅘ'
print(split_hangul_char(char2))  # ['ㅗ', 'ㅏ']

char3 = 'ㄵ'
print(split_hangul_char(char3))  # ['ㄴ', 'ㅈ']
```

### 자음으로 끝나는지 확인
```python
from hangulpy import ends_with_consonant

print(ends_with_consonant('강'))  # False
print(ends_with_consonant('각'))  # True
print(ends_with_consonant('ㄱ'))  # True
print(ends_with_consonant('ㅏ'))  # False
print(ends_with_consonant('a'))  # False
print(ends_with_consonant('한'))  # True
print(ends_with_consonant('하'))  # False
```

### 초성 또는 종성으로 쓰일 수 있는지 확인
```python
from hangulpy import can_be_chosung, can_be_jongsung

print(can_be_chosung('ㄱ'))  # True
print(can_be_chosung('ㄳ'))  # False
print(can_be_chosung('ㄸ'))  # True
print(can_be_jongsung('ㄲ'))  # True
print(can_be_jongsung('ㄸ'))  # False
print(can_be_jongsung('ㄳ'))  # True
```

### 자립명사 붙이기
```python
from hangulpy import jarip_noun

word1 = '확'
sentence1 = '율/률' + '과 통계' # 확률과 통계

word2 = '직'
sentence2 = jarip_noun(word2, '열/렬')
print(sentence2) # 직렬

word3 = '명'
sentence3 = jarip_noun(word3, '영/령')
print(sentence3)    # 명령

word4 = '신'
sentence4 = jarip_noun(word4, '염/념')
print(sentence4)    # 신념

word5 = '범'
sentence5 = jarip_noun(word5, '예/례')
print(sentence5)    # 범례
```

### 숫자 읽기
```python
from hangulpy import number_to_hangul, hangul_to_number

print(number_to_hangul(1234))  # 천이백삼십사
print(number_to_hangul(3.1415926))  # 삼 점 일사일오구이육
print(hangul_to_number("천이백삼십사"))  # 1234
print(hangul_to_number("삼점일사일오구이육"))  # 3.1415926
```