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
    :param particle: 붙일 조사 ('을/를', '이/가', '은/는', '와/과', '으로/로', '이나/나', '이에/에', '이란/란', '아/야', '이랑/랑', '이에요/예요', '으로서/로서', '으로써/로써', '으로부터/로부터', '이여/여', '께서', '이야/야', '와서/와', '이라서/라서', '이든/든', '이며/며', '이라도/라도', '이니까/니까', '이지만/지만', '이랑는/랑는')
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
    elif particle == '와/과':
        return word + ('과' if jongsung_exists else '와')
    elif particle == '으로/로':
        return word + ('으로' if jongsung_exists else '로')
    elif particle == '이나/나':
        return word + ('이나' if jongsung_exists else '나')
    elif particle == '이에/에':
        return word + ('이에' if jongsung_exists else '에')
    elif particle == '이란/란':
        return word + ('이란' if jongsung_exists else '란')
    elif particle == '아/야':
        return word + ('아' if jongsung_exists else '야')
    elif particle == '이랑/랑':
        return word + ('이랑' if jongsung_exists else '랑')
    elif particle == '이에요/예요':
        return word + ('이에요' if jongsung_exists else '예요')
    elif particle == '으로서/로서':
        return word + ('으로서' if jongsung_exists else '로서')
    elif particle == '으로써/로써':
        return word + ('으로써' if jongsung_exists else '로써')
    elif particle == '으로부터/로부터':
        return word + ('으로부터' if jongsung_exists else '로부터')
    elif particle == '이여/여':
        return word + ('이여' if jongsung_exists else '여')
    elif particle == '께서':
        return word + '께서'
    elif particle == '이야/야':
        return word + ('이야' if jongsung_exists else '야')
    elif particle == '와서/와':
        return word + ('와서' if jongsung_exists else '와')
    elif particle == '이라서/라서':
        return word + ('이라서' if jongsung_exists else '라서')
    elif particle == '이든/든':
        return word + ('이든' if jongsung_exists else '든')
    elif particle == '이며/며':
        return word + ('이며' if jongsung_exists else '며')
    elif particle == '이라도/라도':
        return word + ('이라도' if jongsung_exists else '라도')
    elif particle == '이니까/니까':
        return word + ('이니까' if jongsung_exists else '니까')
    elif particle == '이지만/지만':
        return word + ('이지만' if jongsung_exists else '지만')
    elif particle == '이랑는/랑는':
        return word + ('이랑는' if jongsung_exists else '랑는')
    else:
        raise ValueError(f"Unsupported particle: {particle}")
