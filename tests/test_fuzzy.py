import unicodedata
from time import perf_counter

import pytest

from hangulpy import HangulIndex, hangul_distance, hangul_similarity


def test_hangul_distance_uses_jamo_and_normalizes_unicode():
    assert hangul_distance("한글", "한글") == 0.0
    assert hangul_distance(unicodedata.normalize("NFD", "한글"), "한글") == 0.0
    assert hangul_distance("한글", "한국") == 2.0
    assert hangul_distance("과", "고") == 1.0
    assert hangul_similarity("한글", "한국") == pytest.approx(2 / 3)


def test_hangul_index_prioritizes_direct_and_fuzzy_matches():
    index = HangulIndex(["한국", "한글", "한굴", "가나다", "한글날"])

    results = index.search("한글")
    assert [result.text for result in results[:2]] == ["한글", "한글날"]
    assert results[0].matched
    assert results[0].match_index == 0

    typo_results = index.search("한굴", min_score=0.5)
    assert typo_results[0].text == "한굴"
    assert any(result.text == "한글" for result in typo_results)


def test_hangul_index_supports_chosung_and_stable_duplicates():
    index = HangulIndex(["한글", "한국", "하늘", "한글"])
    results = index.search("ㅎㄱ")

    assert [result.text for result in results[:3]] == ["한글", "한국", "한글"]
    assert all(result.score == 1.0 for result in results[:3])
    assert [result.index for result in results[:3]] == [0, 1, 3]


def test_hangul_index_validates_search_options():
    index = HangulIndex(["한글"])

    assert index.search("한글", limit=0) == []
    with pytest.raises(ValueError, match="limit"):
        index.search("한글", limit=-1)
    with pytest.raises(TypeError, match="limit"):
        index.search("한글", limit=True)
    with pytest.raises(ValueError, match="min_score"):
        index.search("한글", min_score=1.1)
    with pytest.raises(TypeError, match="min_score"):
        index.search("한글", min_score=True)

    with pytest.raises(TypeError, match="single string"):
        HangulIndex("한글")
    with pytest.raises(TypeError, match="only strings"):
        HangulIndex(["한글", 1])  # type: ignore[list-item]


def test_hangul_index_uses_linear_substring_dynamic_programming():
    index = HangulIndex(["누" * 400])
    started = perf_counter()

    results = index.search("가" * 40, min_score=0.01)

    assert results == []
    assert perf_counter() - started < 1.0


def test_large_index_reuses_prepared_text_after_cache_churn(monkeypatch):
    import hangulpy.hangul_fuzzy as fuzzy
    from hangulpy import hangul_contains

    items = [f"한글문서{i:05d}" for i in range(1100)]
    index = HangulIndex(items)
    expected = index.search("ㅎㄱ", min_score=1)
    for i in range(1500):
        hangul_contains(f"다른문서{i}", "ㄷ")

    def unexpected_preparation(text):
        raise AssertionError("search must reuse the index's prepared texts")

    monkeypatch.setattr(fuzzy, "prepare_search_text", unexpected_preparation)
    assert index.search("ㅎㄱ", min_score=1) == expected
    assert [r.index for r in expected] == list(range(10))
    assert index.search("없는말", min_score=1) == []


def test_threshold_and_top_k_preserve_scores_and_stable_order():
    import random

    rng = random.Random(1500)
    items = ["".join(rng.choices("가각과한글나", k=rng.randrange(1, 6))) for _ in range(60)]
    items += ["", "각가", "각가", unicodedata.normalize("NFD", "한글")]
    index = HangulIndex(items)
    for query in ["", "과", "ㄱㄱ", "각가", "한굴", "없는말", "ᆨ"]:
        full = index.search(query, limit=len(items))
        for threshold in [0.0, 0.5, 0.75, 1.0]:
            for limit in [1, 5, 100]:
                assert (
                    index.search(query, min_score=threshold, limit=limit)
                    == [r for r in full if r.score >= threshold][:limit]
                )


def test_exact_fuzzy_substring_is_retained_when_chosung_search_misses():
    index = HangulIndex(["악가"])
    result = index.search("ㄱㄱ", min_score=1)[0]
    assert result.score == 1
    assert not result.matched
    assert index.search("ᆨ", min_score=1)[0].match_index == 0
