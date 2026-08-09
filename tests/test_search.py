# tests/test_search.py

import unicodedata
import warnings

import pytest

from hangulpy import (
    HangulMatch,
    HangulpyDeprecationWarning,
    HangulSearcher,
    chosung_includes,
    chosungIncludes,
    find_hangul_spans,
    hangul_contains,
    hangul_search,
    hangul_search_all,
    match_hangul_pattern,
)


class TestHangulSearch:
    """한글 검색 기능 테스트"""

    def test_chosung_includes_alias(self):
        assert chosung_includes("사과", "ㅅㄱ")
        with pytest.warns(HangulpyDeprecationWarning, match="chosung_includes"):
            assert chosungIncludes("사과", "ㅅㄱ")

    def test_project_deprecation_warning_can_be_filtered(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            warnings.filterwarnings("ignore", category=HangulpyDeprecationWarning)
            assert chosungIncludes("사과", "ㅅㄱ")
            assert not hangul_contains("한글", "", notallowempty=True)

        assert caught == []

    def test_hangul_contains_basic(self):
        """기본 포함 여부 테스트"""
        assert hangul_contains("사과", "사")
        assert hangul_contains("사과", "과")
        assert hangul_contains("사과", "사과")
        assert not hangul_contains("사과", "바나나")

    def test_hangul_contains_chosung(self):
        """초성 검색 테스트"""
        assert hangul_contains("사과", "ㅅ")
        assert hangul_contains("사과", "ㄱ")
        assert hangul_contains("사과", "ㅅㄱ")
        assert not hangul_contains("사과", "ㅂ")

    def test_hangul_contains_partial(self):
        """부분 음절 검색 테스트"""
        assert hangul_contains("사과", "삭")
        assert not hangul_contains("사과", "삽")

    def test_hangul_contains_empty(self):
        """빈 패턴 테스트"""
        assert hangul_contains("사과", "")
        assert not hangul_contains("사과", "", not_allow_empty=True)

    def test_deprecated_notallowempty_keyword(self):
        with pytest.warns(HangulpyDeprecationWarning, match="not_allow_empty"):
            assert not hangul_contains("한글", "", notallowempty=True)

        searcher = HangulSearcher("")
        with pytest.warns(HangulpyDeprecationWarning, match="not_allow_empty"):
            assert searcher.find_index("한글", notallowempty=True) == -1

        with pytest.raises(TypeError, match="cannot use both"):
            hangul_contains("한글", "", not_allow_empty=True, notallowempty=True)

    def test_hangul_search_index(self):
        """인덱스 검색 테스트"""
        result = hangul_search("사과는 맛있다", "ㅅ")
        assert result == 0

        result = hangul_search("사과는 맛있다", "ㅂ")
        assert result == -1  # 'ㅂ'가 없음

        assert hangul_search("사과는 맛있다", "맛") == 4

    def test_hangul_search_all(self):
        """모든 매칭 위치 검색 테스트"""
        result = hangul_search_all("가나다가", "ㄱ")
        assert result == [0, 3]

        result = hangul_search_all("가나다가", "ㅂ")
        assert len(result) == 0  # 'ㅂ'가 없음

    def test_hangul_searcher_class(self):
        """HangulSearcher 클래스 테스트"""
        searcher = HangulSearcher("ㅅ")

        assert searcher.search("사과")
        assert not searcher.search("바나나")

        assert searcher.find_index("사과") == 0
        assert searcher.find_index("바나나") == -1

    def test_hangul_searcher_reuse(self):
        """HangulSearcher 재사용 테스트 (캐싱 확인)"""
        searcher = HangulSearcher("ㄱ")

        # 같은 패턴으로 여러 문자열 검색
        assert searcher.search("가나다")
        assert searcher.search("고구마")
        assert not searcher.search("바나나")

        # 모든 위치 찾기
        indices = searcher.find_all("가나다가")
        assert indices == [0, 3]

    def test_hangul_searcher_multi_chosung(self):
        """여러 초성으로 검색하는 테스트"""
        searcher = HangulSearcher("ㅅㄱ")

        assert searcher.search("사과")
        assert searcher.find_index("사과") == 0

    def test_find_hangul_spans_returns_source_ranges(self):
        matches = find_hangul_spans("간장공장공장장", "공장")

        assert matches == [
            HangulMatch(2, 4, "공장"),
            HangulMatch(4, 6, "공장"),
        ]
        assert matches[0].span() == (2, 4)
        assert find_hangul_spans("값", "ㅏㅂ") == [HangulMatch(0, 1, "값")]
        assert find_hangul_spans("한글", "") == []

    def test_find_hangul_spans_can_include_overlapping_matches(self):
        assert find_hangul_spans("가가가", "ㄱㄱ") == [HangulMatch(0, 2, "가가")]
        assert find_hangul_spans("가가가", "ㄱㄱ", overlap=True) == [
            HangulMatch(0, 2, "가가"),
            HangulMatch(1, 3, "가가"),
        ]

    def test_searcher_finditer_reuses_the_compiled_pattern(self):
        searcher = HangulSearcher("공장")

        assert list(searcher.finditer("간장공장공장장")) == [
            HangulMatch(2, 4, "공장"),
            HangulMatch(4, 6, "공장"),
        ]
        assert list(HangulSearcher("").finditer("한글")) == []

    def test_single_chosung_falls_back_to_a_jamo_match(self):
        assert hangul_contains("악", "ㄱ")
        assert hangul_search("악", "ㄱ") == 0
        assert hangul_search_all("악", "ㄱ") == [0]
        assert find_hangul_spans("악", "ㄱ") == [HangulMatch(0, 1, "악")]

        searcher = HangulSearcher("ㄱ")
        assert searcher.search("악")
        assert searcher.find_index("악") == 0
        assert list(searcher.finditer("악")) == [HangulMatch(0, 1, "악")]

        # 초성 매치가 하나라도 있으면 기존 초성 검색 의미를 우선합니다.
        assert hangul_search_all("가악", "ㄱ") == [0]

    def test_canonical_initial_and_final_patterns_match_hcj_search_data(self):
        canonical_initial = "ᄀ"
        canonical_final = "ᆨ"

        assert hangul_search("가", canonical_initial) == 0
        assert hangul_search("악", canonical_final) == 0
        assert find_hangul_spans("악", canonical_final) == [HangulMatch(0, 1, "악")]
        assert HangulSearcher(canonical_initial).find_index("가") == 0
        assert list(HangulSearcher(canonical_final).finditer("악")) == [HangulMatch(0, 1, "악")]

    def test_nfd_matches_use_original_codepoint_offsets(self):
        text = "A" + unicodedata.normalize("NFD", "한글")
        expected_text = unicodedata.normalize("NFD", "글")

        assert hangul_search(text, "글") == 4
        assert hangul_search_all(text, "글") == [4]
        assert find_hangul_spans(text, "글") == [HangulMatch(4, 7, expected_text)]
        assert list(HangulSearcher("글").finditer(text)) == [HangulMatch(4, 7, expected_text)]

    def test_match_hangul_pattern_wildcard_escapes_regex_chars(self):
        words = ["가구", "가방", "나무", "("]

        assert match_hangul_pattern(words, "ㄱ*") == ["가구", "가방"]
        assert match_hangul_pattern(words, "(") == ["("]

    def test_match_hangul_pattern_regex_mode(self):
        words = ["가구", "가방", "나무"]

        assert match_hangul_pattern(words, r"ㄱㅏ(ㄱㅜ|ㅂㅏㅇ)", regex=True) == ["가구", "가방"]
