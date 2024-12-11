# hangul_role.py

from hangulpy.utils import CHOSUNG_LIST, JONGSUNG_LIST

def can_be_chosung(char):
	"""
	주어진 문자가 한글 초성으로 쓰일 수 있는지 확인합니다.
	
	:param char: 확인할 문자
	:return: 초성으로 쓰일 수 있으면 True, 아니면 False
	"""
	return char in CHOSUNG_LIST

def can_be_jongsung(char):
	"""
	주어진 문자가 한글 종성으로 쓰일 수 있는지 확인합니다.
	
	:param char: 확인할 문자
	:return: 종성으로 쓰일 수 있으면 True, 아니면 False
	"""
	return char in JONGSUNG_LIST
