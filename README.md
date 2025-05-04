# hangulpy

hangulpy는 한글 처리를 위한 파이썬 라이브러리입니다. es-hangul의 파이썬 버전으로, 초성 검색과 조사 붙이기 등의 기능을 제공합니다.

## 설치

```bash
pip install hangulpy
```

## 사용법

모든 기능은 [위키 문서](https://wiki.uiharu.dev/w/hangulpy)를 확인하세요!

# hangulpy

[![PyPI Version](https://img.shields.io/pypi/v/hangulpy.svg)](https://pypi.org/project/hangulpy/)
[![License](https://img.shields.io/github/license/gaon12/hangulpy.svg)](https://github.com/gaon12/hangulpy/blob/main/LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/hangulpy.svg)](https://pypi.org/project/hangulpy/)

**hangulpy**는 [es-hangul](https://github.com/toss/es-hangul)에 영감을 받아 만든 파이썬 한글 처리 라이브러리로, es-hangul의 기능 뿐만 아니라 다양한 추가 기능을 제공합니다.

---

## 기여
기여는 언제든 환영입니다! issue, PR, 기부 등 다양한 방법으로 기여하실 수 있습니다!

## 설치

```bash
pip install hangulpy
```

## 업그레이드

```bash
pip install hangulpy -U
```

## 기능
자세한 기능은 [위키 문서](https://wiki.uiharu.dev/w/hangulpy)를 확인하세요!

### 초성 관련 기능

* **get\_chosung\_string**: 문자열의 초성을 반환합니다. `keep_spaces=True` 옵션으로 공백 유지 가능

```python
from hangulpy import get_chosung_string

text = "가"
print(get_chosung_string(text, keep_spaces=True))  # ㄱ

text2 = "대한 사람 대한으로 길이 보전하세"
print(get_chosung_string(text2))                # ㄷㅎㅅㄹㄷㅎㅇㄹㄱㅇㅂㅈㅎ
print(get_chosung_string(text2, keep_spaces=True))  # ㄷㅎ ㅅㄹ ㄷㅎㅇㄹ ㄱㅇ ㅂㅈㅎ
```

* **chosungIncludes** ^(es)^: es-hangul의 초성 검색 기능

```python
from hangulpy import chosungIncludes

searchWord = '라면'
userInput = 'ㄹㅁ'

result = chosungIncludes(searchWord, userInput)
print(result)  # True
```

### 조사 붙이기

* **josa** ^(es)^: es-hangul의 조사 붙이기 기능 (지원 조사: '을/를', '이/가', '은/는', '와/과', '으로/로', '이나/나', '이에/에', '이란/란', '아/야', '이랑/랑', '이에요/예요', '으로서/로서', '으로써/로써', '으로부터/로부터', '이여/여', '께서', '이야/야', '와서/와', '이라서/라서', '이든/든', '이며/며', '이라도/라도', '이니까/니까', '이지만/지만', '이랑은/랑은')

```python
from hangulpy import josa

word1 = '사과'
sentence1 = josa(word1, '을/를') + ' 먹었습니다.'
print(sentence1)  # '사과를 먹었습니다.'

word2 = '바나나'
sentence2 = josa(word2, '이/가') + ' 맛있습니다.'
print(sentence2)  # '바나나가 맛있습니다.'
```

### 자음/모음 여부 확인

* **is\_hangul\_consonant**: 입력이 한글 자음인지 확인
* **is\_hangul\_vowel**: 입력이 한글 모음인지 확인

```python
from hangulpy import is_hangul_consonant, is_hangul_vowel

print(is_hangul_consonant('ㄱ'))  # True
print(is_hangul_consonant('ㅏ'))  # False
print(is_hangul_vowel('ㅏ'))      # True
print(is_hangul_vowel('ㄱ'))      # False
```

### 자립명사 붙이기

* **jarip\_noun**: 단위 명사 형태를 붙일 때 사용

```python
from hangulpy import jarip_noun

print(jarip_noun('확', '율/률') + '과 통계')  # 확률과 통계
print(jarip_noun('직', '열/렬'))  # 직렬
print(jarip_noun('명', '영/령'))  # 명령
print(jarip_noun('신', '염/념'))  # 신념
print(jarip_noun('범', '예/례'))  # 범례
```

### 문자열 포함 여부 확인

* **hangul\_contains** ^(es)^: es-hangul의 문자열 포함 기능. `notallowempty=True` 옵션으로 빈 문자열 처리 제어

```python
from hangulpy import hangul_contains

print(hangul_contains('사과', ''))                # True
print(hangul_contains('사과', '', notallowempty=True))  # False
print(hangul_contains('사과', 'ㅅ'))               # True
print(hangul_contains('사과', '삭'))               # True
print(hangul_contains('사과', '삽'))               # False
print(hangul_contains('사과', '사과'))             # True

# 공백 포함 예시
print(hangul_contains('사과는 맛있다', '사과는 ㅁ'))  # True
print(hangul_contains('사과는 맛있다', '사과는 '))    # True
```

### 초/중/종성 분해

* **decompose\_hangul\_char**: 단일 문자 분해 (초성, 중성 조합, 종성)
* **split\_hangul\_char**: 배열 형태로 반환 (1차원 배열)
* **decompose\_hangul\_string**: 문자열 단위 분해
* **split\_hangul\_string**: 문자열 배열 분해

```python
from hangulpy import decompose_hangul_char, split_hangul_char, decompose_hangul_string, split_hangul_string

print(decompose_hangul_char('괜'))  # ('ㄱ', ('ㅗ️', 'ㅐ'), ('ㄴ', 'ㅈ'))
print(split_hangul_char('값'))     # ['ㄱ', 'ㅏ', 'ㅂ', 'ㅅ']
print(split_hangul_char('ㅘ'))     # ['ㅗ', 'ㅏ']
print(split_hangul_char('ㄵ'))     # ['ㄴ', 'ㅈ']

# 문자열 분해
print(decompose_hangul_string('감사합니다'))
print(split_hangul_string('ㅘㅝㄵ'))  # ['ㅗ', 'ㅏ', 'ㅜ', 'ㅓ', 'ㄴ', 'ㅈ']
```

### 자음으로 끝나는지 확인

* **ends\_with\_consonant**: 입력이 자음으로 끝나는지 확인

```python
from hangulpy import ends_with_consonant

print(ends_with_consonant('강'))  # False
print(ends_with_consonant('각'))  # True
print(ends_with_consonant('ㄱ'))  # True
print(ends_with_consonant('ㅏ'))  # False
print(ends_with_consonant('한'))  # True
```

### 초성/종성 사용 가능 여부

* **can\_be\_chosung**: 초성으로 쓸 수 있는 글자인지 확인
* **can\_be\_jongsung**: 종성으로 쓸 수 있는 글자인지 확인

```python
from hangulpy import can_be_chosung, can_be_jongsung

print(can_be_chosung('ㄱ'))  # True
print(can_be_chosung('ㄳ'))  # False
print(can_be_chosung('ㄸ'))  # True
print(can_be_jongsung('ㄲ'))  # True
print(can_be_jongsung('ㄳ'))  # True
```

### 한글 여부 확인

* **is\_hangul**: 전체 문자열이 한글인지 확인 (`spaces=True`로 공백 무시)

```python
from hangulpy import is_hangul

print(is_hangul("가"))              # True
print(is_hangul("반가워요"))        # True
print(is_hangul("hello"))           # False
print(is_hangul("안녕 하세요"))     # False
print(is_hangul("안녕 하세요", spaces=True))  # True
```

### 글자 정렬

* **sort\_hangul**: 한글 문자열 리스트를 가나다 순 등으로 정렬

```python
from hangulpy import sort_hangul

words = ['가나', '다라', '나가']
print(sort_hangul(words))         # ['가나', '나가', '다라']
print(sort_hangul(words, reverse=True))  # ['다라', '나가', '가나']
```

### 매칭 패턴 찾기

* **match\_hangul\_pattern**: 초성·중성·종성 패턴으로 리스트에서 매칭 단어 찾기

```python
from hangulpy import match_hangul_pattern

words = ['가구', '나무', '가방']
print(match_hangul_pattern(words, 'ㄱ*'))  # ['가구', '가방']
print(match_hangul_pattern(words, '*ㅜ'))  # ['가구', '나무']
```

### 한영타 오타 수정

* **koen**, **enko**, **autofix**: 한영 키보드 오타 교정 (inko.js 기반)

```python
from hangulpy import koen, enko, autofix

typo_hangul = "ㅗ디ㅣㅐ 재깅!"             # hello world!
typo_alpha = "sork djeldp dlTems..."
print(koen(typo_hangul))
print(enko(typo_alpha))
print(autofix("dl rytnsladms 뭏디dlek!"))
```

### 초/중/종성 조합

* **hangul\_syllable**: 초성, 중성, 종성 조합해서 완성형 문자 생성

```python
from hangulpy import hangul_syllable

print(hangul_syllable("ㄱ", "ㅏ"))           # 가
print(hangul_syllable("ㄱ", "ㅏ", "ㄱ"))  # 각
```

### 숫자 읽기

* **number\_to\_hangul**, **hangul\_to\_number**: 숫자 ↔ 한글 변환

```python
from hangulpy import number_to_hangul, hangul_to_number

print(number_to_hangul(1234))         # 천이백삼십사
print(number_to_hangul(3.1415926))     # 삼 점 일사일오구이육
print(hangul_to_number("천이백삼십사"))  # 1234
print(hangul_to_number("삼점일사일오구이육"))  # 3.1415926
```