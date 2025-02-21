# hangul_syllable.py

from hangulpy.utils import compose_syllable

def hangul_syllable(cho, jung, jong=''):
    """
    입력된 초성, 중성, (선택적) 종성을 가지고 조합해 한글 문자를 만듭니다.
    
    :param cho: 초성 (필수). 예: 'ㄱ'
    :param jung: 중성 (필수). 예: 'ㅏ'
    :param jong: 종성 (선택). 입력하지 않으면 빈 문자열로 간주합니다. 예: 'ㄱ'
    :return: 조합된 완성형 한글 글자. 예: '각'
    
    예상 가능한 예외와 오류 메시지:
      - 초성이 유효하지 않은 경우:
            Exception: "Error: '{cho}' is not a valid initial consonant."
      - 중성이 유효하지 않은 경우:
            Exception: "Error: '{jung}' is not a valid medial vowel."
      - 종성이 유효하지 않은 경우 (종성이 입력된 경우에 한함):
            Exception: "Error: '{jong}' is not a valid final consonant."
    """
    return compose_syllable(cho, jung, jong)
