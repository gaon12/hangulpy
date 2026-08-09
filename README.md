# hangulpy

[![PyPI](https://img.shields.io/pypi/v/hangulpy.svg)](https://pypi.org/project/hangulpy/)
[![Python](https://img.shields.io/pypi/pyversions/hangulpy.svg)](https://pypi.org/project/hangulpy/)
[![CI](https://github.com/gaon12/hangulpy/actions/workflows/ci.yml/badge.svg)](https://github.com/gaon12/hangulpy/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/gaon12/hangulpy.svg)](https://github.com/gaon12/hangulpy/blob/main/LICENSE)

조사 선택부터 자모 분해·조합, 초성 검색, 발음 변환, 로마자 표기까지 제공하는
Python 한글 처리 라이브러리입니다. [es-hangul](https://github.com/toss/es-hangul)에서
영감을 받아 Python에 자연스러운 API와 타입 정보를 제공합니다.

- 별도 런타임 의존성 없음
- NFC·NFD와 호환 자모를 고려한 Unicode 처리
- `py.typed`를 포함한 정적 타입 검사 지원
- 조사, 검색, 숫자, 발음, 로마자 표기를 하나의 패키지에서 제공

## 설치

```bash
python -m pip install -U hangulpy
```

| hangulpy | Python | 지원 정책 |
| --- | --- | --- |
| v1.4.x | 3.8~3.14 | 3.14를 포함한 필수 CI 검증 |
| v1.4.x | 3.15 프리릴리스 | 실패를 허용하는 선행 호환성 검증 |
| v1.5 이상 | 3.11 이상 | 다음 마이너 계열의 최소 버전 |

Python 3.8~3.10을 계속 사용해야 한다면 `python -m pip install "hangulpy<1.5"`로
마지막 호환 계열을 설치할 수 있습니다. 자세한 배경은
[v1.5 마이그레이션 가이드](https://hangulpy.uiharu.dev/migration-v1-5)를 확인하세요.

## 빠른 시작

```python
from hangulpy import (
    extract_chosung,
    format_josa,
    hangul_contains,
    join_jamos,
    number_to_hangul_mixed,
    romanize,
    split_syllables,
    standardize_pronunciation,
)

print(format_josa("RAM[은/는] API[이/가]"))  # RAM은 API가
print(hangul_contains("사과", "삭"))  # True

print(split_syllables("한글", output_format="string"))  # ㅎㅏㄴㄱㅡㄹ
print(join_jamos(["ㅎ", "ㅏ", "ㄴ", "ㄱ", "ㅡ", "ㄹ"]))  # 한글
print(extract_chosung("한글"))  # ㅎㄱ

print(standardize_pronunciation("굳이"))  # 구지
print(romanize("한글"))  # hangeul
print(number_to_hangul_mixed(123456780))  # 1억2,345만6,780
```

## 주요 기능

| 분야 | 설명 | 주요 API |
| --- | --- | --- |
| 조사 | 받침, 숫자, 영문 약어에 맞는 조사 선택 | `josa`, `josa_pick`, `format_josa`, `has_batchim` |
| 검색 | 초성·부분 음절·퍼지 검색과 원문 위치 추적 | `hangul_contains`, `HangulSearcher`, `HangulIndex`, `find_hangul_spans` |
| 자모 | 음절 분해·조합, 자모 단위 편집과 변환 | `split_syllables`, `join_jamos`, `jamo_slice`, `map_hangul` |
| 속성 | 초·중·종성 판정과 문자열 전체 성분 추출 | `get_hangul_components`, `extract_chosung`, `can_be_jongsung` |
| 발음·표기 | 표준 발음 변환과 여러 방식의 로마자 표기 | `standardize_pronunciation`, `romanize`, `Romanizer` |
| 숫자·키보드 | 한글 수사 변환과 한영타 교정 | `number_to_hangul`, `susa`, `days`, `koen`, `enko`, `autofix` |

전체 공개 API와 사용법은 [공식 문서](https://hangulpy.uiharu.dev)에서 확인할 수
있습니다.

## 더 보기

- [빠른 시작 가이드](https://hangulpy.uiharu.dev/quickstart)
- [API 개요](https://hangulpy.uiharu.dev/api/overview)
- [v1.4.2 릴리즈 노트](https://hangulpy.uiharu.dev/releases/v1-4-2)
- [실행 가능한 예제](https://github.com/gaon12/hangulpy/blob/main/examples/quickstart.py)

## 개발과 기여

저장소를 받은 뒤 개발 의존성을 설치하고 검사할 수 있습니다.

```bash
python -m pip install -e ".[dev]"
python -m ruff check .
python -m black --check .
python -m pytest
```

버그 제보, 기능 제안, 문서 개선과 Pull Request를 환영합니다. 작업 전
[열린 이슈](https://github.com/gaon12/hangulpy/issues)를 확인해 주세요.

## 라이선스

[MIT License](https://github.com/gaon12/hangulpy/blob/main/LICENSE)
