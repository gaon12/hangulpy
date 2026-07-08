from hangulpy import standardize_pronunciation


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

    def test_preserves_non_hangul_boundaries(self):
        assert standardize_pronunciation("굳이 test 놓고") == "구지 test 노코"
