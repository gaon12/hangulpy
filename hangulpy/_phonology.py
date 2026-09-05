"""Shared lexical boundaries; orthography alone cannot predict Korean n-insertion."""

from typing import FrozenSet

# Boundaries are zero-based offsets of the following syllable, not arbitrary
# adjacent-syllable substitutions (e.g. 부담요금 must not match 담요).
N_INSERTION_WORDS = {
    "담요": 1,
    "학여울": 1,
    "한여름": 1,
    "알약": 1,
    "서울역": 2,
    "꽃잎": 1,
    "깻잎": 1,
    "솜이불": 1,
    "홑이불": 1,
    "색연필": 1,
    "막일": 1,
    "맨입": 1,
    "내복약": 2,
    "솔잎": 1,
    "물약": 1,
}
PARTICLE_SUFFIXES = frozenset(
    {
        "",
        "이",
        "가",
        "은",
        "는",
        "을",
        "를",
        "의",
        "에",
        "에서",
        "에게",
        "으로",
        "로",
        "과",
        "와",
        "도",
        "만",
        "부터",
        "까지",
        "처럼",
        "보다",
        "이나",
        "나",
        "이다",
        "입니다",
        "들이",
        "들은",
        "들을",
        "들",
        "에도",
        "에서는",
    }
)


def n_insertion_positions(text: str) -> FrozenSet[int]:
    """Recognize supported lexemes, optionally followed by a common particle."""
    return frozenset(
        position
        for word, position in N_INSERTION_WORDS.items()
        if text.startswith(word) and text[len(word) :] in PARTICLE_SUFFIXES
    )
