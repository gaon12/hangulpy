# is_hangul.py

from hangulpy.utils import is_hangul as utils_is_hangul

def is_hangul(text, spaces=False):
    """
    입력된 값이 한글인지 확인합니다.

    :param text: 문자 또는 문자열
    :param spaces: True일 경우 띄어쓰기를 허용합니다.
    :return: 모든 문자가 한글이거나, spaces=True일 경우 한글 또는 띄어쓰기면 True, 그렇지 않으면 False
    """
    return utils_is_hangul(text, spaces)
