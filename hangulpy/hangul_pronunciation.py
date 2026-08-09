"""Rule-based modern Korean pronunciation normalization."""

from dataclasses import dataclass
from typing import List, Literal, Optional, Tuple, Union, overload

from hangulpy.hangul_normalize import normalize_hangul
from hangulpy.utils import (
    CHOSUNG_BASE,
    CHOSUNG_LIST,
    HANGUL_BEGIN_UNICODE,
    HANGUL_END_UNICODE,
    JONGSUNG_DECOMPOSE,
    JONGSUNG_LIST,
    JUNGSUNG_BASE,
    JUNGSUNG_LIST,
    compose_syllable,
)


@dataclass
class _Syllable:
    cho: str
    jung: str
    jong: str
    source: str
    force_tense_next: bool = False


@dataclass(frozen=True)
class PronunciationRuleStep:
    """한 발음 규칙이 바꾼 전후 문자열입니다."""

    rule: str
    before: str
    after: str


@dataclass(frozen=True)
class PronunciationResult:
    """발음 표기와 실제로 적용된 규칙 추적입니다."""

    pronunciation: str
    steps: Tuple[PronunciationRuleStep, ...]


LEXICAL_PRONUNCIATIONS = {"디귿이": "디그시"}
N_INSERTION_PAIRS = {("담", "요"), ("학", "여"), ("한", "여"), ("알", "약")}
H_FINAL_REMAINDER = {"ㅎ": "", "ㄶ": "ㄴ", "ㅀ": "ㄹ"}
ASPIRATE_ONSET = {"ㄱ": "ㅋ", "ㄷ": "ㅌ", "ㅂ": "ㅍ", "ㅈ": "ㅊ"}
PALATALIZATION = {"ㄷ": "ㅈ", "ㅌ": "ㅊ"}
TENSE_CONSONANTS = {"ㄱ": "ㄲ", "ㄷ": "ㄸ", "ㅂ": "ㅃ", "ㅅ": "ㅆ", "ㅈ": "ㅉ"}
FINAL_SIMPLIFICATION = {
    "ㄳ": "ㄱ",
    "ㄵ": "ㄴ",
    "ㄶ": "ㄴ",
    "ㄺ": "ㄱ",
    "ㄻ": "ㅁ",
    "ㄼ": "ㄹ",
    "ㄽ": "ㄹ",
    "ㄾ": "ㄹ",
    "ㄿ": "ㅂ",
    "ㅀ": "ㄹ",
    "ㅄ": "ㅂ",
}
REPRESENTATIVE_FINAL = {
    "ㄲ": "ㄱ",
    "ㅋ": "ㄱ",
    "ㄳ": "ㄱ",
    "ㄺ": "ㄱ",
    "ㅅ": "ㄷ",
    "ㅆ": "ㄷ",
    "ㅈ": "ㄷ",
    "ㅊ": "ㄷ",
    "ㅌ": "ㄷ",
    "ㅎ": "ㄷ",
    "ㄵ": "ㄴ",
    "ㄶ": "ㄴ",
    "ㄼ": "ㄹ",
    "ㄽ": "ㄹ",
    "ㄾ": "ㄹ",
    "ㅀ": "ㄹ",
    "ㅄ": "ㅂ",
    "ㄿ": "ㅂ",
    "ㅍ": "ㅂ",
}


def _is_complete_hangul(char: str) -> bool:
    return len(char) == 1 and HANGUL_BEGIN_UNICODE <= ord(char) <= HANGUL_END_UNICODE


def _decompose_char(char: str) -> _Syllable:
    offset = ord(char) - HANGUL_BEGIN_UNICODE
    return _Syllable(
        CHOSUNG_LIST[offset // CHOSUNG_BASE],
        JUNGSUNG_LIST[(offset % CHOSUNG_BASE) // JUNGSUNG_BASE],
        JONGSUNG_LIST[offset % JUNGSUNG_BASE],
        char,
    )


def _compose_syllables(syllables: List[_Syllable]) -> str:
    return "".join(compose_syllable(item.cho, item.jung, item.jong) for item in syllables)


def _representative_final(jong: str) -> str:
    return REPRESENTATIVE_FINAL.get(jong, jong)


def _record_rule(
    rule: str,
    syllables: List[_Syllable],
    before: str,
    steps: List[PronunciationRuleStep],
) -> None:
    after = _compose_syllables(syllables)
    if before != after:
        steps.append(PronunciationRuleStep(rule, before, after))


def _apply_h_rules(syllables: List[_Syllable]) -> None:
    for index in range(len(syllables) - 1):
        current = syllables[index]
        following = syllables[index + 1]

        if following.cho == "ㅇ" and current.jong in H_FINAL_REMAINDER:
            remainder = H_FINAL_REMAINDER[current.jong]
            current.jong = ""
            if remainder:
                following.cho = remainder
            continue

        if current.jong in H_FINAL_REMAINDER and following.cho in ASPIRATE_ONSET:
            current.jong = H_FINAL_REMAINDER[current.jong]
            following.cho = ASPIRATE_ONSET[following.cho]
            continue

        if following.cho != "ㅎ" or not current.jong:
            continue

        if current.jong in JONGSUNG_DECOMPOSE:
            first, second = JONGSUNG_DECOMPOSE[current.jong]
            if second in ASPIRATE_ONSET:
                current.jong = first
                following.cho = ASPIRATE_ONSET[second]
                if following.jung == "ㅣ" and following.cho == "ㅌ":
                    following.cho = "ㅊ"
                continue

        representative = _representative_final(current.jong)
        if representative in ASPIRATE_ONSET:
            current.jong = ""
            following.cho = ASPIRATE_ONSET[representative]
            if following.jung == "ㅣ" and following.cho == "ㅌ":
                following.cho = "ㅊ"


def _apply_palatalization(syllables: List[_Syllable]) -> None:
    for index in range(len(syllables) - 1):
        current = syllables[index]
        following = syllables[index + 1]
        if current.jong in PALATALIZATION and following.cho == "ㅇ" and following.jung == "ㅣ":
            following.cho = PALATALIZATION[current.jong]
            current.jong = ""


def _apply_lexical_n_insertion(syllables: List[_Syllable]) -> None:
    for index in range(len(syllables) - 1):
        current = syllables[index]
        following = syllables[index + 1]
        if (current.source, following.source) in N_INSERTION_PAIRS and following.cho == "ㅇ":
            following.cho = "ㄴ"


def _apply_liaison(syllables: List[_Syllable]) -> None:
    for index in range(len(syllables) - 1):
        current = syllables[index]
        following = syllables[index + 1]
        if not current.jong or current.jong == "ㅇ" or following.cho != "ㅇ":
            continue

        if current.jong in JONGSUNG_DECOMPOSE:
            first, second = JONGSUNG_DECOMPOSE[current.jong]
            current.jong = first
            following.cho = second
            if second == "ㅅ":
                current.force_tense_next = True
        else:
            following.cho = current.jong
            current.jong = ""


def _apply_final_rules(syllables: List[_Syllable]) -> None:
    for index, current in enumerate(syllables):
        following: Optional[_Syllable] = (
            syllables[index + 1] if index + 1 < len(syllables) else None
        )
        original = current.jong
        if not original:
            continue

        if following and following.cho in TENSE_CONSONANTS:
            if original in JONGSUNG_DECOMPOSE or _representative_final(original) in {
                "ㄱ",
                "ㄷ",
                "ㅂ",
            }:
                current.force_tense_next = True

        if following and original == "ㄺ" and following.cho == "ㄱ":
            current.jong = "ㄹ"
        elif original == "ㄼ" and current.cho == "ㅂ" and current.jung == "ㅏ":
            current.jong = "ㅂ"
        else:
            current.jong = FINAL_SIMPLIFICATION.get(original, original)

        current.jong = _representative_final(current.jong)


def _apply_nasal_and_liquid_assimilation(syllables: List[_Syllable]) -> None:
    for index in range(len(syllables) - 1):
        current = syllables[index]
        following = syllables[index + 1]
        final = _representative_final(current.jong)

        if following.cho in {"ㄴ", "ㅁ"}:
            if final == "ㄱ":
                current.jong = "ㅇ"
            elif final == "ㄷ":
                current.jong = "ㄴ"
            elif final == "ㅂ":
                current.jong = "ㅁ"
            elif final == "ㄹ" and following.cho == "ㄴ":
                following.cho = "ㄹ"
            continue

        if following.cho == "ㄹ":
            if final == "ㄱ":
                current.jong = "ㅇ"
                following.cho = "ㄴ"
            elif final == "ㄷ":
                current.jong = "ㄴ"
                following.cho = "ㄴ"
            elif final == "ㅂ":
                current.jong = "ㅁ"
                following.cho = "ㄴ"
            elif final in {"ㅁ", "ㅇ"}:
                following.cho = "ㄴ"
            elif final in {"ㄴ", "ㄹ"}:
                current.jong = "ㄹ"
                following.cho = "ㄹ"


def _apply_tensing(syllables: List[_Syllable]) -> None:
    for index in range(len(syllables) - 1):
        current = syllables[index]
        following = syllables[index + 1]
        if current.force_tense_next and following.cho in TENSE_CONSONANTS:
            following.cho = TENSE_CONSONANTS[following.cho]


def _standardize_segment(
    segment: str, apply_tensing: bool
) -> Tuple[str, Tuple[PronunciationRuleStep, ...]]:
    steps: List[PronunciationRuleStep] = []
    lexical = LEXICAL_PRONUNCIATIONS.get(segment, segment)
    if lexical != segment:
        steps.append(PronunciationRuleStep("lexical_exception", segment, lexical))

    syllables = [_decompose_char(char) for char in lexical]
    rules = [
        ("h_assimilation_and_elision", _apply_h_rules),
        ("palatalization", _apply_palatalization),
        ("lexical_n_insertion", _apply_lexical_n_insertion),
        ("liaison", _apply_liaison),
        ("final_simplification", _apply_final_rules),
        ("nasal_and_liquid_assimilation", _apply_nasal_and_liquid_assimilation),
    ]
    for name, rule in rules:
        before = _compose_syllables(syllables)
        rule(syllables)
        _record_rule(name, syllables, before, steps)

    if apply_tensing:
        before = _compose_syllables(syllables)
        _apply_tensing(syllables)
        _record_rule("tensing", syllables, before, steps)

    return _compose_syllables(syllables), tuple(steps)


def _standardize_text(
    text: str, *, apply_tensing: bool = True
) -> Tuple[str, Tuple[PronunciationRuleStep, ...]]:
    normalized = normalize_hangul(text, "NFC")
    result: List[str] = []
    segment: List[str] = []
    steps: List[PronunciationRuleStep] = []

    def flush_segment() -> None:
        if not segment:
            return
        standardized, segment_steps = _standardize_segment("".join(segment), apply_tensing)
        result.append(standardized)
        steps.extend(segment_steps)
        segment.clear()

    for char in normalized:
        if _is_complete_hangul(char):
            segment.append(char)
        else:
            flush_segment()
            result.append(char)
    flush_segment()
    return "".join(result), tuple(steps)


@overload
def standardize_pronunciation(text: str, *, explain: Literal[False] = False) -> str: ...


@overload
def standardize_pronunciation(text: str, *, explain: Literal[True]) -> PronunciationResult: ...


def standardize_pronunciation(
    text: str, *, explain: bool = False
) -> Union[str, PronunciationResult]:
    """주요 표준 발음 규칙을 적용하고 선택적으로 규칙 추적을 반환합니다."""
    pronunciation, steps = _standardize_text(text)
    if explain:
        return PronunciationResult(pronunciation, steps)
    return pronunciation
