# tests/test_search.py

from hangulpy import (
    hangul_contains,
    hangul_search,
    hangul_search_all,
    HangulSearcher,
)


class TestHangulSearch:
    """한글 검색 기능 테스트"""

    def test_hangul_contains_basic(self):
        """기본 포함 여부 테스트"""
        assert hangul_contains('사과', '사') == True
        assert hangul_contains('사과', '과') == True
        assert hangul_contains('사과', '사과') == True
        assert hangul_contains('사과', '바나나') == False

    def test_hangul_contains_chosung(self):
        """초성 검색 테스트"""
        assert hangul_contains('사과', 'ㅅ') == True
        assert hangul_contains('사과', 'ㄱ') == True
        assert hangul_contains('사과', 'ㅅㄱ') == True
        assert hangul_contains('사과', 'ㅂ') == False

    def test_hangul_contains_partial(self):
        """부분 음절 검색 테스트"""
        assert hangul_contains('사과', '삭') == True
        assert hangul_contains('사과', '삽') == False

    def test_hangul_contains_empty(self):
        """빈 패턴 테스트"""
        assert hangul_contains('사과', '') == True
        assert hangul_contains('사과', '', notallowempty=True) == False

    def test_hangul_search_index(self):
        """인덱스 검색 테스트"""
        result = hangul_search('사과는 맛있다', 'ㅅ')
        assert result >= 0  # 'ㅅ'가 발견됨

        result = hangul_search('사과는 맛있다', 'ㅂ')
        assert result == -1  # 'ㅂ'가 없음

    def test_hangul_search_all(self):
        """모든 매칭 위치 검색 테스트"""
        result = hangul_search_all('가나다가', 'ㄱ')
        assert len(result) >= 1  # 최소 1개 이상 발견

        result = hangul_search_all('가나다가', 'ㅂ')
        assert len(result) == 0  # 'ㅂ'가 없음

    def test_hangul_searcher_class(self):
        """HangulSearcher 클래스 테스트"""
        searcher = HangulSearcher('ㅅ')

        assert searcher.search('사과') == True
        assert searcher.search('바나나') == False

        assert searcher.find_index('사과') >= 0
        assert searcher.find_index('바나나') == -1

    def test_hangul_searcher_reuse(self):
        """HangulSearcher 재사용 테스트 (캐싱 확인)"""
        searcher = HangulSearcher('ㄱ')

        # 같은 패턴으로 여러 문자열 검색
        assert searcher.search('가나다') == True
        assert searcher.search('고구마') == True
        assert searcher.search('바나나') == False

        # 모든 위치 찾기
        indices = searcher.find_all('가나다가')
        assert len(indices) >= 1
