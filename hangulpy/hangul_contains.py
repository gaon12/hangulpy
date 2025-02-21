# hangul_contains.py

from hangulpy.utils import is_hangul
from hangulpy.hangul_split import split_hangul_string

def hangul_contains(word, pattern, notallowempty=False):
	"""
	주어진 한글 문자열이 다른 한글 문자열을 포함하는지 검사합니다.
	
	:param word: 검사할 한글 문자열
	:param pattern: 포함 여부를 검사할 한글 문자열 패턴
	:param notallowempty: 패턴이 빈 문자열일 때 false를 반환하는 옵션
	:return: 포함되면 True, 아니면 False
	"""
	if not pattern:
		return not notallowempty
	
	# 문자열을 분해하여 리스트로 변환
	word_split = ''.join(''.join(split_hangul_string(char)) for char in word)
	pattern_split = ''.join(''.join(split_hangul_string(char)) for char in pattern)
	
	return pattern_split in word_split
