import unicodedata

import pytest

from hangulpy import PronunciationResult, standardize_pronunciation


class TestStandardizePronunciation:
    def test_palatalization_and_h_assimilation(self):
        assert standardize_pronunciation("굳이") == "구지"
        assert standardize_pronunciation("같이") == "가치"
        assert standardize_pronunciation("닫히다") == "다치다"
        assert standardize_pronunciation("놓고") == "노코"
        assert standardize_pronunciation("좋다") == "조타"

    def test_n_insertion_nasalization_and_liquidization(self):
        assert standardize_pronunciation("담요") == "담뇨"
        assert standardize_pronunciation("국물") == "궁물"
        assert standardize_pronunciation("신라") == "실라"
        assert standardize_pronunciation("백로") == "뱅노"

    def test_compound_final_and_tensing(self):
        assert standardize_pronunciation("읽고") == "일꼬"
        assert standardize_pronunciation("값도") == "갑또"
        assert standardize_pronunciation("밟다") == "밥따"

    def test_hard_conversion_can_disable_tensing(self):
        assert standardize_pronunciation("닦다", hard_conversion=False) == "닥다"
        assert standardize_pronunciation("값도", hard_conversion=False) == "갑도"
        assert standardize_pronunciation("넓게", hard_conversion=False) == "널게"

        explained = standardize_pronunciation("값도", hard_conversion=False, explain=True)
        assert isinstance(explained, PronunciationResult)
        assert explained.pronunciation == "갑도"
        assert all(step.rule != "tensing" for step in explained.steps)

    def test_preserves_non_hangul_boundaries(self):
        assert standardize_pronunciation("굳이 test 놓고") == "구지 test 노코"

    @pytest.mark.parametrize(
        ("text", "expected"),
        [
            ("좋아", "조아"),
            ("않아", "아나"),
            ("먹여", "머겨"),
            ("밟고", "밥꼬"),
            ("옷", "옫"),
            ("디귿이", "디그시"),
            ("닦다", "닥따"),
            ("있다", "읻따"),
            ("핥다", "할따"),
            ("젊다", "점따"),
            ("축하", "추카"),
            ("맏이", "마지"),
            ("한여름", "한녀름"),
            ("먹어", "머거"),
            ("넋도", "넉또"),
            ("먹는", "멍는"),
            ("난로", "날로"),
            ("별내", "별래"),
            ("알약", "알략"),
            ("굳히다", "구치다"),
            ("숱하다", "수타다"),
            ("옷한벌", "오탄벌"),
            ("학여울", "항녀울"),
            ("서울역", "서울력"),
        ],
    )
    def test_rule_engine_regressions(self, text, expected):
        assert standardize_pronunciation(text) == expected

    def test_nfd_and_explainable_rule_trace(self):
        nfd = unicodedata.normalize("NFD", "국물")
        explained = standardize_pronunciation(nfd, explain=True)

        assert isinstance(explained, PronunciationResult)
        assert explained.pronunciation == "궁물"
        assert explained.steps
        assert explained.steps[-1].before != explained.steps[-1].after
