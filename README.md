# hangulpy

[![PyPI Version](https://img.shields.io/pypi/v/hangulpy.svg)](https://pypi.org/project/hangulpy/)
[![License](https://img.shields.io/github/license/gaon12/hangulpy.svg)](https://github.com/gaon12/hangulpy/blob/main/LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/hangulpy.svg)](https://pypi.org/project/hangulpy/)

`hangulpy`는 [es-hangul](https://github.com/toss/es-hangul)에서 영감을 받아 만든 파이썬 한글 처리 라이브러리입니다. 조사 자동 선택, 초성/부분 음절 검색, 자모 분해/조합, 로마자 표기, 숫자 변환, 한영타 교정까지 한 곳에서 제공합니다.

## 주요 기능

- 조사 자동 선택: `josa`, `josa_pick`, `has_jongsung`, `has_batchim`
- 초성/부분 음절 검색: `get_chosung_string`, `chosung_includes`, `chosungIncludes`, `hangul_contains`, `hangul_search`, `HangulSearcher`
- 한글 속성 검사: `is_hangul`, `is_complete_hangul`, `get_hangul_components`
- 자모 분해/조합: `decompose_hangul_string`, `split_hangul_string`, `split_syllables`, `join_jamos`, `combine_vowels`, `remove_last_character`
- 변환 기능: `romanize`, `Romanizer`, `standardize_pronunciation`, `number_to_hangul`, `number_to_hangul_mixed`, `hangul_to_number`, `susa`, `days`, `koen`, `enko`, `autofix`

## 설치

```bash
pip install hangulpy
```

업그레이드는 아래처럼 진행할 수 있습니다.

```bash
pip install -U hangulpy
```

## 빠른 예시

```python
from hangulpy import (
    HangulSearcher,
    days,
    get_hangul_components,
    join_jamos,
    josa,
    number_to_hangul_mixed,
    remove_last_character,
    romanize,
    standardize_pronunciation,
)

print(josa("사과", "을/를"))  # 사과를

searcher = HangulSearcher("ㅅㄱ")
print(searcher.search("사과는 맛있다"))  # True

print(get_hangul_components("한"))  # ('ㅎ', 'ㅏ', 'ㄴ')
print(join_jamos(["ㅎ", "ㅏ", "ㄴ", "ㄱ", "ㅡ", "ㄹ"]))  # 한글
print(remove_last_character("전화"))  # 전호
print(number_to_hangul_mixed(123456780))  # 1억2,345만6,780
print(days(29))  # 스무아흐레
print(romanize("광희문", "revised"))  # gwanghuimun
print(standardize_pronunciation("굳이"))  # 구지
print(romanize("오죽헌", "revised", mode="proper", capitalize=True))  # Ojukheon
print(romanize("충청북도", "revised", mode="admin"))  # chungcheongbuk-do
```

## 문서

- [공식 문서](https://hangulpy.uiharu.dev)
- [로마자 표기 문서](https://hangulpy.uiharu.dev/api/conversions/romanize)

## 예제

- 빠른 실행 예제: `examples/quickstart.py`

## 기여

이슈, PR, 문서 개선 모두 환영합니다.
