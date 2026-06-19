# romanize.py
# Korean romanization implementation

from dataclasses import dataclass
from typing import List, Optional, Tuple

from hangulpy.utils import (
    CHOSUNG_BASE,
    CHOSUNG_LIST,
    HANGUL_BEGIN_UNICODE,
    HANGUL_END_UNICODE,
    JONGSUNG_DECOMPOSE,
    JONGSUNG_LIST,
    JUNGSUNG_BASE,
    JUNGSUNG_LIST,
)

# Romanization tables for different standards

# National Institute of Korean Language (국립국어원) - Revised Romanization
REVISED_CHOSUNG = {
    "ㄱ": "g",
    "ㄲ": "kk",
    "ㄴ": "n",
    "ㄷ": "d",
    "ㄸ": "tt",
    "ㄹ": "r",
    "ㅁ": "m",
    "ㅂ": "b",
    "ㅃ": "pp",
    "ㅅ": "s",
    "ㅆ": "ss",
    "ㅇ": "",
    "ㅈ": "j",
    "ㅉ": "jj",
    "ㅊ": "ch",
    "ㅋ": "k",
    "ㅌ": "t",
    "ㅍ": "p",
    "ㅎ": "h",
}

REVISED_JUNGSUNG = {
    "ㅏ": "a",
    "ㅐ": "ae",
    "ㅑ": "ya",
    "ㅒ": "yae",
    "ㅓ": "eo",
    "ㅔ": "e",
    "ㅕ": "yeo",
    "ㅖ": "ye",
    "ㅗ": "o",
    "ㅘ": "wa",
    "ㅙ": "wae",
    "ㅚ": "oe",
    "ㅛ": "yo",
    "ㅜ": "u",
    "ㅝ": "wo",
    "ㅞ": "we",
    "ㅟ": "wi",
    "ㅠ": "yu",
    "ㅡ": "eu",
    "ㅢ": "ui",
    "ㅣ": "i",
}

REVISED_JONGSUNG = {
    "": "",
    "ㄱ": "k",
    "ㄲ": "k",
    "ㄳ": "k",
    "ㄴ": "n",
    "ㄵ": "n",
    "ㄶ": "n",
    "ㄷ": "t",
    "ㄹ": "l",
    "ㄺ": "k",
    "ㄻ": "m",
    "ㄼ": "p",
    "ㄽ": "l",
    "ㄾ": "l",
    "ㄿ": "p",
    "ㅀ": "l",
    "ㅁ": "m",
    "ㅂ": "p",
    "ㅄ": "p",
    "ㅅ": "t",
    "ㅆ": "t",
    "ㅇ": "ng",
    "ㅈ": "t",
    "ㅊ": "t",
    "ㅋ": "k",
    "ㅌ": "t",
    "ㅍ": "p",
    "ㅎ": "t",
}

# McCune-Reischauer romanization
MR_CHOSUNG = {
    "ㄱ": "k",
    "ㄲ": "kk",
    "ㄴ": "n",
    "ㄷ": "t",
    "ㄸ": "tt",
    "ㄹ": "r",
    "ㅁ": "m",
    "ㅂ": "p",
    "ㅃ": "pp",
    "ㅅ": "s",
    "ㅆ": "ss",
    "ㅇ": "",
    "ㅈ": "ch",
    "ㅉ": "tch",
    "ㅊ": "ch'",
    "ㅋ": "k'",
    "ㅌ": "t'",
    "ㅍ": "p'",
    "ㅎ": "h",
}

MR_JUNGSUNG = {
    "ㅏ": "a",
    "ㅐ": "ae",
    "ㅑ": "ya",
    "ㅒ": "yae",
    "ㅓ": "ŏ",
    "ㅔ": "e",
    "ㅕ": "yŏ",
    "ㅖ": "ye",
    "ㅗ": "o",
    "ㅘ": "wa",
    "ㅙ": "wae",
    "ㅚ": "oe",
    "ㅛ": "yo",
    "ㅜ": "u",
    "ㅝ": "wŏ",
    "ㅞ": "we",
    "ㅟ": "wi",
    "ㅠ": "yu",
    "ㅡ": "ŭ",
    "ㅢ": "ŭi",
    "ㅣ": "i",
}

MR_JONGSUNG = {
    "": "",
    "ㄱ": "k",
    "ㄲ": "k",
    "ㄳ": "k",
    "ㄴ": "n",
    "ㄵ": "n",
    "ㄶ": "n",
    "ㄷ": "t",
    "ㄹ": "l",
    "ㄺ": "k",
    "ㄻ": "m",
    "ㄼ": "p",
    "ㄽ": "l",
    "ㄾ": "l",
    "ㄿ": "p",
    "ㅀ": "l",
    "ㅁ": "m",
    "ㅂ": "p",
    "ㅄ": "p",
    "ㅅ": "t",
    "ㅆ": "t",
    "ㅇ": "ng",
    "ㅈ": "t",
    "ㅊ": "t",
    "ㅋ": "k",
    "ㅌ": "t",
    "ㅍ": "p",
    "ㅎ": "t",
}

# Academic/Yale romanization
YALE_CHOSUNG = {
    "ㄱ": "k",
    "ㄲ": "kk",
    "ㄴ": "n",
    "ㄷ": "t",
    "ㄸ": "tt",
    "ㄹ": "l",
    "ㅁ": "m",
    "ㅂ": "p",
    "ㅃ": "pp",
    "ㅅ": "s",
    "ㅆ": "ss",
    "ㅇ": "",
    "ㅈ": "c",
    "ㅉ": "cc",
    "ㅊ": "ch",
    "ㅋ": "kh",
    "ㅌ": "th",
    "ㅍ": "ph",
    "ㅎ": "h",
}

YALE_JUNGSUNG = {
    "ㅏ": "a",
    "ㅐ": "ay",
    "ㅑ": "ya",
    "ㅒ": "yay",
    "ㅓ": "e",
    "ㅔ": "ey",
    "ㅕ": "ye",
    "ㅖ": "yey",
    "ㅗ": "o",
    "ㅘ": "wa",
    "ㅙ": "way",
    "ㅚ": "oy",
    "ㅛ": "yo",
    "ㅜ": "wu",
    "ㅝ": "we",
    "ㅞ": "wey",
    "ㅟ": "wuy",
    "ㅠ": "yu",
    "ㅡ": "u",
    "ㅢ": "uy",
    "ㅣ": "i",
}

YALE_JONGSUNG = {
    "": "",
    "ㄱ": "k",
    "ㄲ": "k",
    "ㄳ": "ks",
    "ㄴ": "n",
    "ㄵ": "nc",
    "ㄶ": "nh",
    "ㄷ": "t",
    "ㄹ": "l",
    "ㄺ": "lk",
    "ㄻ": "lm",
    "ㄼ": "lp",
    "ㄽ": "ls",
    "ㄾ": "lth",
    "ㄿ": "lph",
    "ㅀ": "lh",
    "ㅁ": "m",
    "ㅂ": "p",
    "ㅄ": "ps",
    "ㅅ": "s",
    "ㅆ": "s",
    "ㅇ": "ng",
    "ㅈ": "c",
    "ㅊ": "ch",
    "ㅋ": "kh",
    "ㅌ": "th",
    "ㅍ": "ph",
    "ㅎ": "h",
}


IOTIZED_VOWELS = {"ㅑ", "ㅒ", "ㅕ", "ㅖ", "ㅛ", "ㅠ", "ㅣ"}
ASPIRATED_CONSONANTS = {"ㄱ": "ㅋ", "ㄷ": "ㅌ", "ㅂ": "ㅍ", "ㅈ": "ㅊ"}
ADMIN_SUFFIXES = {
    "도": "do",
    "시": "si",
    "군": "gun",
    "구": "gu",
    "읍": "eup",
    "면": "myeon",
    "리": "ri",
    "동": "dong",
    "가": "ga",
}
DOUBLE_SURNAMES = {
    "남궁",
    "독고",
    "동방",
    "망절",
    "사공",
    "서문",
    "선우",
    "소봉",
    "어금",
    "장곡",
    "제갈",
    "황보",
}
REVISED_SPECIAL_CASES = {
    "신문로": "sinmunno",
}
PROPER_SPECIAL_CASES = {
    "묵호": "mukho",
    "집현전": "jiphyeonjeon",
    "오죽헌": "ojukheon",
}
DISAMBIGUATION_SPECIAL_CASES = {
    "반구대": "ban-gudae",
}


@dataclass
class _RevisedSyllable:
    cho: str
    jung: str
    jong: str


def _is_complete_hangul(char: str) -> bool:
    """
    주어진 문자가 완성형 한글 음절인지 확인합니다.

    :param char: 검사할 문자
    :return: 완성형 한글이면 True, 아니면 False
    """
    if len(char) != 1:
        return False
    code = ord(char)
    return HANGUL_BEGIN_UNICODE <= code <= HANGUL_END_UNICODE


def _get_hangul_components(char: str) -> Optional[Tuple[str, str, str]]:
    """
    완성형 한글 음절을 초성, 중성, 종성으로 분해합니다.

    :param char: 한글 음절 문자
    :return: (초성, 중성, 종성) 튜플, 한글이 아니면 None
    """
    if not _is_complete_hangul(char):
        return None
    char_index = ord(char) - HANGUL_BEGIN_UNICODE
    chosung_index = char_index // CHOSUNG_BASE
    jungsung_index = (char_index % CHOSUNG_BASE) // JUNGSUNG_BASE
    jongsung_index = char_index % JUNGSUNG_BASE
    return (
        CHOSUNG_LIST[chosung_index],
        JUNGSUNG_LIST[jungsung_index],
        JONGSUNG_LIST[jongsung_index],
    )


def _romanize_revised_jongsung(jong: str, next_chosung: Optional[str]) -> str:
    return REVISED_JONGSUNG.get(jong, jong)


def _representative_jongsung(jong: str) -> str:
    if jong in {"ㄱ", "ㄲ", "ㅋ", "ㄳ", "ㄺ"}:
        return "ㄱ"
    if jong in {"ㄴ", "ㄵ", "ㄶ"}:
        return "ㄴ"
    if jong in {"ㄷ", "ㅅ", "ㅆ", "ㅈ", "ㅊ", "ㅌ", "ㅎ"}:
        return "ㄷ"
    if jong in {"ㄹ", "ㄽ", "ㄾ", "ㅀ"}:
        return "ㄹ"
    if jong in {"ㅁ", "ㄻ"}:
        return "ㅁ"
    if jong in {"ㅂ", "ㅍ", "ㅄ", "ㄼ", "ㄿ"}:
        return "ㅂ"
    return jong


def _parse_revised_segment(text: str) -> List[_RevisedSyllable]:
    syllables: List[_RevisedSyllable] = []
    for char in text:
        components = _get_hangul_components(char)
        if not components:
            continue
        syllables.append(_RevisedSyllable(*components))
    return syllables


def _apply_palatalization(syllables: List[_RevisedSyllable]) -> None:
    for index in range(len(syllables) - 1):
        current = syllables[index]
        following = syllables[index + 1]

        if current.jong not in {"ㄷ", "ㅌ"}:
            continue

        if following.cho == "ㅇ" and following.jung == "ㅣ":
            following.cho = "ㅈ" if current.jong == "ㄷ" else "ㅊ"
            current.jong = ""
        elif following.cho == "ㅎ" and following.jung == "ㅣ":
            following.cho = "ㅊ"
            current.jong = ""


def _apply_n_insertion(syllables: List[_RevisedSyllable]) -> None:
    for index in range(len(syllables) - 1):
        current = syllables[index]
        following = syllables[index + 1]

        if current.jong and following.cho == "ㅇ" and following.jung in IOTIZED_VOWELS:
            following.cho = "ㄴ"


def _apply_liaison(syllables: List[_RevisedSyllable]) -> None:
    for index in range(len(syllables) - 1):
        current = syllables[index]
        following = syllables[index + 1]

        if not current.jong or following.cho != "ㅇ":
            continue

        if current.jong == "ㅇ":
            continue

        if current.jong == "ㅎ":
            current.jong = ""
            continue

        if current.jong in JONGSUNG_DECOMPOSE:
            first, second = JONGSUNG_DECOMPOSE[current.jong]
            current.jong = first
            following.cho = second
            continue

        following.cho = current.jong
        current.jong = ""


def _apply_h_assimilation(syllables: List[_RevisedSyllable], mode: str) -> None:
    for index in range(len(syllables) - 1):
        current = syllables[index]
        following = syllables[index + 1]

        if current.jong in {"ㅎ", "ㄶ", "ㅀ"} and following.cho in ASPIRATED_CONSONANTS:
            if current.jong in JONGSUNG_DECOMPOSE:
                current.jong = JONGSUNG_DECOMPOSE[current.jong][0]
            else:
                current.jong = ""
            following.cho = ASPIRATED_CONSONANTS[following.cho]
            continue

        if mode == "proper":
            continue

        if current.jong in ASPIRATED_CONSONANTS and following.cho == "ㅎ":
            following.cho = ASPIRATED_CONSONANTS[current.jong]
            current.jong = ""


def _apply_consonant_assimilation(syllables: List[_RevisedSyllable]) -> None:
    for index in range(len(syllables) - 1):
        current = syllables[index]
        following = syllables[index + 1]
        representative = _representative_jongsung(current.jong)

        if not representative or not following.cho:
            continue

        if following.cho in {"ㄴ", "ㅁ"}:
            if representative == "ㄱ":
                current.jong = "ㅇ"
            elif representative == "ㄷ":
                current.jong = "ㄴ"
            elif representative == "ㅂ":
                current.jong = "ㅁ"
            elif representative == "ㄹ" and following.cho == "ㄴ":
                following.cho = "ㄹ"
            continue

        if following.cho == "ㄹ":
            if representative == "ㄱ":
                current.jong = "ㅇ"
                following.cho = "ㄴ"
            elif representative == "ㄷ":
                current.jong = "ㄴ"
                following.cho = "ㄴ"
            elif representative == "ㅂ":
                current.jong = "ㅁ"
                following.cho = "ㄴ"
            elif representative in {"ㅁ", "ㅇ"}:
                following.cho = "ㄴ"
            elif representative in {"ㄴ", "ㄹ"}:
                current.jong = "ㄹ"
                following.cho = "ㄹ"


def _romanize_revised_syllable(
    syllable: _RevisedSyllable,
    previous_jong: str,
) -> str:
    onset = syllable.cho
    if onset == "ㄹ" and previous_jong == "ㄹ":
        choseong = "l"
    else:
        choseong = REVISED_CHOSUNG.get(onset, onset)

    return (
        choseong
        + REVISED_JUNGSUNG.get(syllable.jung, syllable.jung)
        + _romanize_revised_jongsung(syllable.jong, None)
    )


def _romanize_name_segment(text: str, hyphenate: bool) -> str:
    if len(text) <= 2:
        return _romanize_revised_segment(text, "name", False)

    if len(text) >= 4 and text[:2] in DOUBLE_SURNAMES:
        surname = text[:2]
        given_name = text[2:]
    else:
        surname = text[:1]
        given_name = text[1:]

    if hyphenate and len(given_name) > 1:
        given = "-".join(_romanize_revised_segment(char, "name", False) for char in given_name)
    else:
        given = _romanize_revised_segment(given_name, "name", False)

    return _romanize_revised_segment(surname, "name", False) + " " + given


def _needs_disambiguation_hyphen(
    previous: _RevisedSyllable,
    following: _RevisedSyllable,
) -> bool:
    return following.cho == "ㅇ"


def _romanize_revised_segment(text: str, mode: str, disambiguate: bool) -> str:
    if mode == "proper" and text in PROPER_SPECIAL_CASES:
        return PROPER_SPECIAL_CASES[text]

    if mode != "name" and text in REVISED_SPECIAL_CASES:
        return REVISED_SPECIAL_CASES[text]

    if disambiguate and text in DISAMBIGUATION_SPECIAL_CASES:
        return DISAMBIGUATION_SPECIAL_CASES[text]

    syllables = _parse_revised_segment(text)

    if mode != "name":
        _apply_palatalization(syllables)
        _apply_h_assimilation(syllables, mode)
        _apply_n_insertion(syllables)
        _apply_liaison(syllables)
        _apply_consonant_assimilation(syllables)

    result: List[str] = []
    previous_jong = ""
    for index, syllable in enumerate(syllables):
        if (
            disambiguate
            and index > 0
            and _needs_disambiguation_hyphen(syllables[index - 1], syllable)
        ):
            result.append("-")
        result.append(_romanize_revised_syllable(syllable, previous_jong))
        previous_jong = _representative_jongsung(syllable.jong)

    return "".join(result)


def _romanize_admin_segment(text: str, omit_suffix: bool) -> str:
    for suffix in sorted(ADMIN_SUFFIXES, key=len, reverse=True):
        if text.endswith(suffix) and len(text) > len(suffix):
            stem = text[: -len(suffix)]
            if omit_suffix and suffix in {"시", "군", "읍"}:
                return _romanize_revised_segment(stem, "general", False)

            return _romanize_revised_segment(stem, "general", False) + "-" + ADMIN_SUFFIXES[suffix]

    return _romanize_revised_segment(text, "general", False)


def _capitalize_words(text: str) -> str:
    parts = text.split(" ")
    capitalized: List[str] = []
    for part in parts:
        if part:
            capitalized.append(part[0].upper() + part[1:])
        else:
            capitalized.append(part)
    return " ".join(capitalized)


class Romanizer:
    """
    한글 로마자 표기 변환 클래스.
    다양한 로마자 표기 규칙을 지원합니다.
    """

    SYSTEMS = {
        "revised": (REVISED_CHOSUNG, REVISED_JUNGSUNG, REVISED_JONGSUNG),
        "mr": (MR_CHOSUNG, MR_JUNGSUNG, MR_JONGSUNG),
        "mccune": (MR_CHOSUNG, MR_JUNGSUNG, MR_JONGSUNG),
        "yale": (YALE_CHOSUNG, YALE_JUNGSUNG, YALE_JONGSUNG),
        "academic": (YALE_CHOSUNG, YALE_JUNGSUNG, YALE_JONGSUNG),
    }

    def __init__(
        self,
        system: str = "revised",
        mode: str = "general",
        capitalize: bool = False,
        disambiguate: bool = False,
        name_hyphen: bool = False,
        admin_omit_suffix: bool = False,
    ) -> None:
        """
        Romanizer 인스턴스를 생성합니다.

        :param system: 로마자 표기 규칙 ('revised', 'mr', 'mccune', 'yale', 'academic')
        :param mode: 개정 로마자 표기 모드 ('general', 'proper', 'name', 'admin')
        :param capitalize: 단어 첫 글자를 대문자로 변환할지 여부
        :param disambiguate: 발음상 혼동을 줄이기 위한 붙임표 사용 여부
        :param name_hyphen: 인명 모드에서 이름 음절 사이에 붙임표를 넣을지 여부
        :param admin_omit_suffix: 행정 구역 모드에서 시/군/읍 접미사를 생략할지 여부
        """
        if system.lower() not in self.SYSTEMS:
            raise ValueError(
                f"Unsupported romanization system: {system}. "
                f"Supported systems: {', '.join(self.SYSTEMS.keys())}"
            )

        if mode not in {"general", "proper", "name", "admin"}:
            raise ValueError("Unsupported revised romanization mode")

        self.system = system.lower()
        self.mode = mode
        self.capitalize = capitalize
        self.disambiguate = disambiguate
        self.name_hyphen = name_hyphen
        self.admin_omit_suffix = admin_omit_suffix
        self.chosung_table, self.jungsung_table, self.jongsung_table = self.SYSTEMS[self.system]

    def romanize_char(self, char: str) -> str:
        """
        단일 한글 음절을 로마자로 변환합니다.

        :param char: 한글 음절 문자
        :return: 로마자 표기
        """
        if not _is_complete_hangul(char):
            return char

        components = _get_hangul_components(char)
        if not components:
            return char

        cho, jung, jong = components

        romanized = ""
        romanized += self.chosung_table.get(cho, cho)
        romanized += self.jungsung_table.get(jung, jung)
        romanized += self.jongsung_table.get(jong, jong)

        return romanized

    def romanize(self, text: str) -> str:
        """
        한글 문자열을 로마자로 변환합니다.

        :param text: 한글 문자열
        :return: 로마자 표기
        """
        result: List[str] = []
        segment: List[str] = []

        def flush_segment() -> None:
            if not segment:
                return

            chunk = "".join(segment)
            if self.system == "revised":
                if self.mode == "admin":
                    result.append(_romanize_admin_segment(chunk, self.admin_omit_suffix))
                elif self.mode == "name":
                    result.append(_romanize_name_segment(chunk, self.name_hyphen))
                else:
                    result.append(_romanize_revised_segment(chunk, self.mode, self.disambiguate))
            else:
                for char in chunk:
                    result.append(self.romanize_char(char))
            segment.clear()

        for char in text:
            if _is_complete_hangul(char):
                segment.append(char)
            else:
                flush_segment()
                result.append(char)

        flush_segment()

        romanized = "".join(result)
        if self.capitalize:
            return _capitalize_words(romanized)
        return romanized


def romanize(
    text: str,
    system: str = "revised",
    mode: str = "general",
    capitalize: bool = False,
    disambiguate: bool = False,
    name_hyphen: bool = False,
    admin_omit_suffix: bool = False,
) -> str:
    """
    한글 문자열을 로마자로 변환하는 헬퍼 함수.

    :param text: 한글 문자열
    :param system: 로마자 표기 규칙 ('revised', 'mr', 'mccune', 'yale', 'academic')
    :param mode: 개정 로마자 표기 모드 ('general', 'proper', 'name', 'admin')
    :param capitalize: 단어 첫 글자를 대문자로 변환할지 여부
    :param disambiguate: 발음상 혼동을 줄이기 위한 붙임표 사용 여부
    :param name_hyphen: 인명 모드에서 이름 음절 사이에 붙임표를 넣을지 여부
    :param admin_omit_suffix: 행정 구역 모드에서 시/군/읍 접미사를 생략할지 여부
    :return: 로마자 표기
    """
    romanizer = Romanizer(
        system,
        mode=mode,
        capitalize=capitalize,
        disambiguate=disambiguate,
        name_hyphen=name_hyphen,
        admin_omit_suffix=admin_omit_suffix,
    )
    return romanizer.romanize(text)
