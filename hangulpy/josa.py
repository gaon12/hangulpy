# josa.py

from hangulpy.utils import is_hangul, HANGUL_BEGIN_UNICODE, JONGSUNG_COUNT

def has_jongsung(char):
	"""
	주어진 한글 음절에 받침이 있는지 확인합니다.
	
	:param char: 한글 음절 문자
	:return: 받침이 있으면 True, 없으면 False
	"""
	if is_hangul(char):
		# 한글 음절의 유니코드 값을 기준으로 받침의 유무를 확인합니다.
		char_index = ord(char) - HANGUL_BEGIN_UNICODE
		return (char_index % JONGSUNG_COUNT) != 0
	return False

def josa(word, particle):
	"""
	주어진 단어에 적절한 조사를 붙여 반환합니다.
	
	:param word: 조사와 결합할 단어
	:param particle: 붙일 조사 ('을/를', '이/가', '은/는', '와/과', '으로/로', '이나/나', '이에/에', '이란/란', '아/야', '이랑/랑', '이에요/예요', '으로서/로서', '으로써/로써', '으로부터/로부터', '이여/여', '께서', '이야/야', '와서/와', '이라서/라서', '이든/든', '이며/며', '이라도/라도', '이니까/니까', '이지만/지만', '이랑은/랑은'
								'이라고/라고', '이라며/라며', '이라니/라니', '이라니까/라니까', '이라거든/라거든', '이라더니/라더니', '이라더군/라더군', '이라던데/라던데', '이라고는/라고는', '이라는데/라는데', '이라면/라면', '이라서야/라서야', '이라야/라야', '이라든가/라든가', '이든지/든지', '이거나/거나', '이라면야/라면야', '이라면말이지/라면말이지',
								'이라야만/라야만', '이었으면/였으면', '이라서도/라서도', '이므로/므로', '이기에/기에', '이니/니', '이라니깐/라니깐', '이면서/면서', '이자/자', '이면서도/면서도', '이라든지/라든지', '이었지만/였지만', '이었으나/였으나', '이긴 하지만/긴 하지만', '이야말로/야말로', '이어야/여야', '이었고/였고', '이었는데/였는데', '이었더니/였더니',
								'이었을 때/였을 때', '이었을지라도/였을지라도', '이었던/였던', '이었으니까/였으니까', '이라고도/라고도', '이라곤 해도/라곤 해도', '이라지/라지', '이라네/라네', '이거든/거든', '이여/여', '이시여/시여', '아/야', '이야/야', '이에요/예요', '이어요/여요', '이었어요/였어요', '이었어/였어')
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
	elif particle == '이랑은/랑은':
		return word + ('이랑은' if jongsung_exists else '랑은')
	elif particle == '이라고/라고':
		return word + ('이라고' if jongsung_exists else '라고')
	elif particle == '이라며/라며':
		return word + ('이라며' if jongsung_exists else '라며')
	elif particle == '이라니/라니':
		return word + ('이라니' if jongsung_exists else '라니')
	elif particle == '이라니까/라니까':
		return word + ('이라니까' if jongsung_exists else '라니까')
	elif particle == '이라거든/라거든':
		return word + ('이라거든' if jongsung_exists else '라거든')
	elif particle == '이라더니/라더니':
		return word + ('이라더니' if jongsung_exists else '라더니')
	elif particle == '이라더군/라더군':
		return word + ('이라더군' if jongsung_exists else '라더군')
	elif particle == '이라던데/라던데':
		return word + ('이라던데' if jongsung_exists else '라던데')
	elif particle == '이라고는/라고는':
		return word + ('이라고는' if jongsung_exists else '라고는')
	elif particle == '이라는데/라는데':
		return word + ('이라는데' if jongsung_exists else '라는데')
	elif particle == '이라면/라면':
		return word + ('이라면' if jongsung_exists else '라면')
	elif particle == '이라서야/라서야':
		return word + ('이라서야' if jongsung_exists else '라서야')
	elif particle == '이라야/라야':
		return word + ('이라야' if jongsung_exists else '라야')
	elif particle == '이라든가/라든가':
		return word + ('이라든가' if jongsung_exists else '라든가')
	elif particle == '이든지/든지':
		return word + ('이든지' if jongsung_exists else '든지')
	elif particle == '이거나/거나':
		return word + ('이거나' if jongsung_exists else '거나')
	elif particle == '이라면야/라면야':
		return word + ('이라면야' if jongsung_exists else '라면야')
	elif particle == '이라면말이지/라면말이지':
		return word + ('이라면말이지' if jongsung_exists else '라면말이지')
	elif particle == '이라야만/라야만':
		return word + ('이라야만' if jongsung_exists else '라야만')
	elif particle == '이었으면/였으면':
		return word + ('이었으면' if jongsung_exists else '였으면')
	elif particle == '이라서도/라서도':
		return word + ('이라서도' if jongsung_exists else '라서도')
	elif particle == '이므로/므로':
		return word + ('이므로' if jongsung_exists else '므로')
	elif particle == '이기에/기에':
		return word + ('이기에' if jongsung_exists else '기에')
	elif particle == '이니/니':
		return word + ('이니' if jongsung_exists else '니')
	elif particle == '이라니깐/라니깐':
		return word + ('이라니깐' if jongsung_exists else '라니깐')
	elif particle == '이면서/면서':
		return word + ('이면서' if jongsung_exists else '면서')
	elif particle == '이자/자':
		return word + ('이자' if jongsung_exists else '자')
	elif particle == '이면서도/면서도':
		return word + ('이면서도' if jongsung_exists else '면서도')
	elif particle == '이라든지/라든지':
		return word + ('이라든지' if jongsung_exists else '라든지')
	elif particle == '이었지만/였지만':
		return word + ('이었지만' if jongsung_exists else '였지만')
	elif particle == '이었으나/였으나':
		return word + ('이었으나' if jongsung_exists else '였으나')
	elif particle == '이긴 하지만/긴 하지만':
		return word + ('이긴 하지만' if jongsung_exists else '긴 하지만')
	elif particle == '이야말로/야말로':
		return word + ('이야말로' if jongsung_exists else '야말로')
	elif particle == '이어야/여야':
		return word + ('이어야' if jongsung_exists else '여야')
	elif particle == '이었고/였고':
		return word + ('이었고' if jongsung_exists else '였고')
	elif particle == '이었는데/였는데':
		return word + ('이었는데' if jongsung_exists else '였는데')
	elif particle == '이었더니/였더니':
		return word + ('이었더니' if jongsung_exists else '였더니')
	elif particle == '이었을 때/였을 때':
		return word + ('이었을 때' if jongsung_exists else '였을 때')
	elif particle == '이었을지라도/였을지라도':
		return word + ('이었을지라도' if jongsung_exists else '였을지라도')
	elif particle == '이었던/였던':
		return word + ('이었던' if jongsung_exists else '였던')
	elif particle == '이었으니까/였으니까':
		return word + ('이었으니까' if jongsung_exists else '였으니까')
	elif particle == '이라고도/라고도':
		return word + ('이라고도' if jongsung_exists else '라고도')
	elif particle == '이라곤 해도/라곤 해도':
		return word + ('이라곤 해도' if jongsung_exists else '라곤 해도')
	elif particle == '이라지/라지':
		return word + ('이라지' if jongsung_exists else '라지')
	elif particle == '이라네/라네':
		return word + ('이라네' if jongsung_exists else '라네')
	elif particle == '이거든/거든':
		return word + ('이거든' if jongsung_exists else '거든')
	elif particle == '이시여/시여':
		return word + ('이시여' if jongsung_exists else '시여')
	elif particle == '이어요/여요':
		return word + ('이어요' if jongsung_exists else '여요')
	elif particle == '이었어요/였어요':
		return word + ('이었어요' if jongsung_exists else '였어요')
	elif particle == '이었어/였어':
		return word + ('이었어' if jongsung_exists else '였어')
	else:
		raise ValueError(f"Unsupported particle: {particle}")
