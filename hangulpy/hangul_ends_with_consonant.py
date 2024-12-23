# hangul_ends_with_consonant.py

from hangulpy.utils import is_hangul, HANGUL_BEGIN_UNICODE, CHOSUNG_LIST, JONGSUNG_LIST

def ends_with_consonant(char):
	"""
	주어진 문자가 자음으로 끝나는지 확인합니다.
	
	:param char: 확인할 문자
	:return: 자음으로 끝나면 True, 아니면 False
	"""
	if not is_hangul(char):
		return char in CHOSUNG_LIST

	# 한글 음절의 유니코드 값을 기준으로 종성 인덱스를 확인합니다.
	char_index = ord(char) - HANGUL_BEGIN_UNICODE
	jongsung_index = char_index % 28  # 28개의 종성

	return JONGSUNG_LIST[jongsung_index] != ''
