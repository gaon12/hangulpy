# hangul_check.py

from hangulpy.utils import CHOSUNG_LIST, JUNGSUNG_LIST

def is_hangul_consonant(char):
	"""
	주어진 문자가 한글 자음인지 확인합니다.
	
	:param char: 확인할 문자
	:return: 한글 자음이면 True, 아니면 False
	"""
	return char in CHOSUNG_LIST

def is_hangul_vowel(char):
	"""
	주어진 문자가 한글 모음인지 확인합니다.
	
	:param char: 확인할 문자
	:return: 한글 모음이면 True, 아니면 False
	"""
	return char in JUNGSUNG_LIST
