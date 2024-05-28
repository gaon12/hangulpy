# josa.py

from hangulpy.utils import is_hangul_char, HANGUL_BEGIN_UNICODE, JONGSUNG_COUNT

def has_jongsung(char):
    """
    주어진 한글 음절에 받침이 있는지 확인합니다.
    
    :param char: 한글 음절 문자
    :return: 받침이 있으면 True, 없으면 False
    """
    if is_hangul_char(char):
        # 한글 음절의 유니코드 값을 기준으로 받침의 유무를 확인합니다.
        char_index = ord(char) - HANGUL_BEGIN_UNICODE
        return (char_index % JONGSUNG_COUNT) != 0
    return False

def josa(word, particle):
    """
    주어진 단어에 적절한 조사를 붙여 반환합니다.
    
    :param word: 조사와 결합할 단어
    :param particle: 붙일 조사 ('을/를', '이/가', '은/는', '과/와')
    :return: 적절한 조사가 붙은 단어 문자열
    """
    if not word:
        return ''
    
    # 단어의 마지막 글자를 가져옵니다.
    word_ending = word[-1]
    # 마지막 글자의 받침 유무를 확인합니다.
    jongsung_exists = has_jongsung(word_ending)
    
    if particle == '을/를':
        return word + ('을' if jongsung_exists else '를')
    elif particle == '이/가':
        return word + ('이' if jongsung_exists else '가')
    elif particle == '은/는':
        return word + ('은' if jongsung_exists else '는')
    elif particle == '과/와':
        return word + ('과' if jongsung_exists else '와')
    else:
        raise ValueError(f"Unsupported particle: {particle}")
