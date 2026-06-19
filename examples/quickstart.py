"""Quickstart examples for hangulpy."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from hangulpy import (
    HangulSearcher,
    autofix,
    convert_qwerty_to_hangul,
    get_hangul_components,
    join_jamos,
    josa,
    number_to_hangul,
    number_to_hangul_mixed,
    remove_last_character,
    romanize,
)


def main() -> None:
    print("hangulpy quickstart")
    print("=" * 40)
    print(f"조사 붙이기: {josa('사과', '을/를')}")

    searcher = HangulSearcher("ㅅㄱ")
    print(f"초성 검색: {searcher.search('사과는 맛있다')}")

    print(f"음절 성분 추출: {get_hangul_components('한')}")
    print(f"자모 조합: {join_jamos(['ㅎ', 'ㅏ', 'ㄴ', 'ㄱ', 'ㅡ', 'ㄹ'])}")
    print(f"마지막 자모 제거: {remove_last_character('전화')}")
    print(f"로마자 표기: {romanize('한글', 'revised')}")
    print(f"숫자 읽기: {number_to_hangul(1234)}")
    print(f"혼합 숫자 표기: {number_to_hangul_mixed(123456780)}")
    print(f"QWERTY 조합: {convert_qwerty_to_hangul('ABC')}")
    print(f"한영타 교정: {autofix('gksrmf')}")
    print()
    print("자세한 문서는 docs/index.mdx 와 docs/quickstart.mdx 를 확인하세요.")


if __name__ == "__main__":
    main()
