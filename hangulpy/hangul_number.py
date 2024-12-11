# hangul_number.py

from hangulpy.utils import UNITS, NUMBERS

def number_to_hangul(num):
	"""
	주어진 숫자를 한글로 변환합니다.
	
	:param num: 변환할 숫자
	:return: 한글 숫자 문자열
	"""
	if num == 0:
		return "영"
	
	if isinstance(num, float):
		return float_to_hangul(num)
	
	result = ""
	str_num = str(num)[::-1]
	
	for i, digit in enumerate(str_num):
		digit = int(digit)
		if digit != 0:
			if i == 4:
				result = "만" + result
			elif i > 4 and i % 4 == 0:
				result = UNITS[4 * (i // 4)] + result
			part = NUMBERS[digit] + UNITS[i % 4]
			if i % 4 == 0 and digit == 1 and i != 0:
				part = UNITS[i % 4]  # 1은 생략
			result = part + result

	if result.startswith('일'):
		result = result[1:]
	
	return result

def float_to_hangul(num):
	"""
	주어진 소수를 한글로 변환합니다.
	
	:param num: 변환할 소수
	:return: 한글 숫자 문자열
	"""
	int_part, frac_part = str(num).split('.')
	return f"{number_to_hangul(int(int_part))} 점 {''.join(NUMBERS[int(d)] for d in frac_part)}"

def hangul_to_number(hangul):
	"""
	주어진 한글 숫자 문자열을 숫자로 변환합니다.
	
	:param hangul: 변환할 한글 숫자 문자열
	:return: 숫자
	"""
	num_map = {name: value for value, name in enumerate(NUMBERS) if name}
	unit_map = {name: 10**idx for idx, name in enumerate(UNITS) if name}
	num = 0
	tmp = 0
	stack = []
	is_float = False
	float_part = 0
	float_div = 1

	# 소수점 분리
	if '점' in hangul:
		integer_part, fractional_part = hangul.split('점')
	else:
		integer_part, fractional_part = hangul, ''

	# 정수 부분 처리
	for char in integer_part:
		if char in num_map:
			stack.append(num_map[char])
		elif char in unit_map:
			if not stack:
				stack.append(1)
			tmp += sum(stack) * unit_map[char]
			stack = []
		else:
			if stack:
				tmp += sum(stack)
			stack = []
			num += tmp
			tmp = 0

	if stack:
		tmp += sum(stack)
	num += tmp

	# 소수 부분 처리
	if fractional_part:
		for char in fractional_part:
			if char in num_map:
				float_part = float_part * 10 + num_map[char]
				float_div *= 10
		return num + float_part / float_div

	return num
