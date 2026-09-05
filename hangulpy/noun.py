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

    if particle in {"율/률", "열/렬"}:
        initial_form, internal_form = particle.split("/")
        use_initial = not jongsung_exists or get_jongsung(word_ending) == "ㄴ"
        return word + (initial_form if use_initial else internal_form)
    internal_forms = {"영/령": "령", "염/념": "념", "예/례": "례"}
    if particle in internal_forms:
        return word + internal_forms[particle]
    raise ValueError(f"Unsupported particle: {particle}")
