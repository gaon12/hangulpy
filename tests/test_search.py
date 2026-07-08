# tests/test_search.py

from hangulpy import (
    HangulSearcher,
    chosung_includes,
    hangul_contains,
    hangul_search,
    hangul_search_all,
    match_hangul_pattern,
)


class TestHangulSearch:
    """한글 검색 기능 테스트"""

    def test_chosung_includes_alias(self):
        assert chosung_includes("사과", "ㅅㄱ")

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
        assert not hangul_contains("사과", "", notallowempty=True)

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

    def test_match_hangul_pattern_wildcard_escapes_regex_chars(self):
        words = ["가구", "가방", "나무", "("]

        assert match_hangul_pattern(words, "ㄱ*") == ["가구", "가방"]
        assert match_hangul_pattern(words, "(") == ["("]

    def test_match_hangul_pattern_regex_mode(self):
        words = ["가구", "가방", "나무"]

        assert match_hangul_pattern(words, r"ㄱㅏ(ㄱㅜ|ㅂㅏㅇ)", regex=True) == ["가구", "가방"]
