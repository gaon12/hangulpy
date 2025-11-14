# romanize.py
# Korean romanization implementation

from typing import List, Optional, Tuple
from hangulpy.utils import (
    HANGUL_BEGIN_UNICODE,
    HANGUL_END_UNICODE,
    CHOSUNG_LIST,
    JUNGSUNG_LIST,
    JONGSUNG_LIST,
    CHOSUNG_BASE,
    JUNGSUNG_BASE,
)


# Romanization tables for different standards

# National Institute of Korean Language (국립국어원) - Revised Romanization
REVISED_CHOSUNG = {
    'ㄱ': 'g', 'ㄲ': 'kk', 'ㄴ': 'n', 'ㄷ': 'd', 'ㄸ': 'tt',
    'ㄹ': 'r', 'ㅁ': 'm', 'ㅂ': 'b', 'ㅃ': 'pp', 'ㅅ': 's',
    'ㅆ': 'ss', 'ㅇ': '', 'ㅈ': 'j', 'ㅉ': 'jj', 'ㅊ': 'ch',
    'ㅋ': 'k', 'ㅌ': 't', 'ㅍ': 'p', 'ㅎ': 'h'
}

REVISED_JUNGSUNG = {
    'ㅏ': 'a', 'ㅐ': 'ae', 'ㅑ': 'ya', 'ㅒ': 'yae', 'ㅓ': 'eo',
    'ㅔ': 'e', 'ㅕ': 'yeo', 'ㅖ': 'ye', 'ㅗ': 'o', 'ㅘ': 'wa',
    'ㅙ': 'wae', 'ㅚ': 'oe', 'ㅛ': 'yo', 'ㅜ': 'u', 'ㅝ': 'wo',
    'ㅞ': 'we', 'ㅟ': 'wi', 'ㅠ': 'yu', 'ㅡ': 'eu', 'ㅢ': 'ui',
    'ㅣ': 'i'
}

REVISED_JONGSUNG = {
    '': '', 'ㄱ': 'k', 'ㄲ': 'k', 'ㄳ': 'k', 'ㄴ': 'n', 'ㄵ': 'n',
    'ㄶ': 'n', 'ㄷ': 't', 'ㄹ': 'l', 'ㄺ': 'k', 'ㄻ': 'm', 'ㄼ': 'p',
    'ㄽ': 'l', 'ㄾ': 'l', 'ㄿ': 'p', 'ㅀ': 'l', 'ㅁ': 'm', 'ㅂ': 'p',
    'ㅄ': 'p', 'ㅅ': 't', 'ㅆ': 't', 'ㅇ': 'ng', 'ㅈ': 't', 'ㅊ': 't',
    'ㅋ': 'k', 'ㅌ': 't', 'ㅍ': 'p', 'ㅎ': 't'
}

# McCune-Reischauer romanization
MR_CHOSUNG = {
    'ㄱ': 'k', 'ㄲ': 'kk', 'ㄴ': 'n', 'ㄷ': 't', 'ㄸ': 'tt',
    'ㄹ': 'r', 'ㅁ': 'm', 'ㅂ': 'p', 'ㅃ': 'pp', 'ㅅ': 's',
    'ㅆ': 'ss', 'ㅇ': '', 'ㅈ': 'ch', 'ㅉ': 'tch', 'ㅊ': "ch'",
    'ㅋ': "k'", 'ㅌ': "t'", 'ㅍ': "p'", 'ㅎ': 'h'
}

MR_JUNGSUNG = {
    'ㅏ': 'a', 'ㅐ': 'ae', 'ㅑ': 'ya', 'ㅒ': 'yae', 'ㅓ': 'ŏ',
    'ㅔ': 'e', 'ㅕ': 'yŏ', 'ㅖ': 'ye', 'ㅗ': 'o', 'ㅘ': 'wa',
    'ㅙ': 'wae', 'ㅚ': 'oe', 'ㅛ': 'yo', 'ㅜ': 'u', 'ㅝ': 'wŏ',
    'ㅞ': 'we', 'ㅟ': 'wi', 'ㅠ': 'yu', 'ㅡ': 'ŭ', 'ㅢ': 'ŭi',
    'ㅣ': 'i'
}

MR_JONGSUNG = {
    '': '', 'ㄱ': 'k', 'ㄲ': 'k', 'ㄳ': 'k', 'ㄴ': 'n', 'ㄵ': 'n',
    'ㄶ': 'n', 'ㄷ': 't', 'ㄹ': 'l', 'ㄺ': 'k', 'ㄻ': 'm', 'ㄼ': 'p',
    'ㄽ': 'l', 'ㄾ': 'l', 'ㄿ': 'p', 'ㅀ': 'l', 'ㅁ': 'm', 'ㅂ': 'p',
    'ㅄ': 'p', 'ㅅ': 't', 'ㅆ': 't', 'ㅇ': 'ng', 'ㅈ': 't', 'ㅊ': 't',
    'ㅋ': 'k', 'ㅌ': 't', 'ㅍ': 'p', 'ㅎ': 't'
}

# Academic/Yale romanization
YALE_CHOSUNG = {
    'ㄱ': 'k', 'ㄲ': 'kk', 'ㄴ': 'n', 'ㄷ': 't', 'ㄸ': 'tt',
    'ㄹ': 'l', 'ㅁ': 'm', 'ㅂ': 'p', 'ㅃ': 'pp', 'ㅅ': 's',
    'ㅆ': 'ss', 'ㅇ': '', 'ㅈ': 'c', 'ㅉ': 'cc', 'ㅊ': 'ch',
    'ㅋ': 'kh', 'ㅌ': 'th', 'ㅍ': 'ph', 'ㅎ': 'h'
}

YALE_JUNGSUNG = {
    'ㅏ': 'a', 'ㅐ': 'ay', 'ㅑ': 'ya', 'ㅒ': 'yay', 'ㅓ': 'e',
    'ㅔ': 'ey', 'ㅕ': 'ye', 'ㅖ': 'yey', 'ㅗ': 'o', 'ㅘ': 'wa',
    'ㅙ': 'way', 'ㅚ': 'oy', 'ㅛ': 'yo', 'ㅜ': 'wu', 'ㅝ': 'we',
    'ㅞ': 'wey', 'ㅟ': 'wuy', 'ㅠ': 'yu', 'ㅡ': 'u', 'ㅢ': 'uy',
    'ㅣ': 'i'
}

YALE_JONGSUNG = {
    '': '', 'ㄱ': 'k', 'ㄲ': 'k', 'ㄳ': 'ks', 'ㄴ': 'n', 'ㄵ': 'nc',
    'ㄶ': 'nh', 'ㄷ': 't', 'ㄹ': 'l', 'ㄺ': 'lk', 'ㄻ': 'lm', 'ㄼ': 'lp',
    'ㄽ': 'ls', 'ㄾ': 'lth', 'ㄿ': 'lph', 'ㅀ': 'lh', 'ㅁ': 'm', 'ㅂ': 'p',
    'ㅄ': 'ps', 'ㅅ': 's', 'ㅆ': 's', 'ㅇ': 'ng', 'ㅈ': 'c', 'ㅊ': 'ch',
    'ㅋ': 'kh', 'ㅌ': 'th', 'ㅍ': 'ph', 'ㅎ': 'h'
}


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


class Romanizer:
    """
    한글 로마자 표기 변환 클래스.
    다양한 로마자 표기 규칙을 지원합니다.
    """

    SYSTEMS = {
        'revised': (REVISED_CHOSUNG, REVISED_JUNGSUNG, REVISED_JONGSUNG),
        'mr': (MR_CHOSUNG, MR_JUNGSUNG, MR_JONGSUNG),
        'mccune': (MR_CHOSUNG, MR_JUNGSUNG, MR_JONGSUNG),
        'yale': (YALE_CHOSUNG, YALE_JUNGSUNG, YALE_JONGSUNG),
        'academic': (YALE_CHOSUNG, YALE_JUNGSUNG, YALE_JONGSUNG),
    }

    def __init__(self, system: str = 'revised') -> None:
        """
        Romanizer 인스턴스를 생성합니다.

        :param system: 로마자 표기 규칙 ('revised', 'mr', 'mccune', 'yale', 'academic')
        """
        if system.lower() not in self.SYSTEMS:
            raise ValueError(f"Unsupported romanization system: {system}. "
                           f"Supported systems: {', '.join(self.SYSTEMS.keys())}")

        self.system = system.lower()
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

        romanized = ''
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
        for char in text:
            result.append(self.romanize_char(char))
        return ''.join(result)


def romanize(text: str, system: str = 'revised') -> str:
    """
    한글 문자열을 로마자로 변환하는 헬퍼 함수.

    :param text: 한글 문자열
    :param system: 로마자 표기 규칙 ('revised', 'mr', 'mccune', 'yale', 'academic')
    :return: 로마자 표기
    """
    romanizer = Romanizer(system)
    return romanizer.romanize(text)
