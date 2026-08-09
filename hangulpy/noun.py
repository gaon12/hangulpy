# noun.py

from hangulpy.hangul_normalize import normalize_hangul
from hangulpy.hangul_properties import get_jongsung
from hangulpy.josa import has_jongsung


def jarip_noun(word: str, particle: str) -> str:
    """
    주어진 단어에 적절한 자립명사를 붙여 반환합니다.

    :param word: 자립명사와 결합할 단어
    :param particle: 붙일 자립명사 ('율/률', '열/렬', '영/령', '염/념', '예/례')
    :return: 적절한 자립명사가 붙은 단어 문자열
    """
    if not word:
        return ""

    # 단어의 마지막 글자를 가져옵니다.
    word_ending = normalize_hangul(word, "NFC")[-1]

    # 마지막 글자의 받침 유무를 확인합니다.
    jongsung_exists = has_jongsung(word_ending)

    if particle == "율/률":
        return word + ("율" if not jongsung_exists or get_jongsung(word_ending) == "ㄴ" else "률")
    elif particle == "열/렬":
        return word + ("열" if not jongsung_exists else "렬")
    elif particle == "영/령":
        return word + ("영" if not jongsung_exists else "령")
    elif particle == "염/념":
        return word + ("염" if not jongsung_exists else "념")
    elif particle == "예/례":
        return word + ("예" if not jongsung_exists else "례")
    else:
        raise ValueError(f"Unsupported particle: {particle}")
