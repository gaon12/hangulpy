# hangul_typoerror.py

from hangulpy.utils import (
    CHOSUNG_LIST, JUNGSUNG_LIST, JONGSUNG_LIST, 
    CONSONANT_MAP, VOWEL_MAP, CONSONANT_RMAP, VOWEL_RMAP, 
    DOUBLE_INITIAL_MAP, COMPOUND_FINAL_MAP, COMPOUND_FINAL_DECOMP, VOWEL_COMBO,
    is_hangul, compose_syllable
)

def enko(eng_text, allowDoubleConsonant=False):
    """
    영문 키보드 입력값을 한글 자모 조합으로 변환합니다.
    
    :param eng_text: 변환할 영문 문자열
    :param allowDoubleConsonant: 두 개의 초성 결합(쌍자음) 허용 여부
    :return: 한글 자판 입력 문자열
    """
    result = []
    state = {'cho': None, 'jung': None, 'jong': "", 'jong_combined': False}
    
    def flush():
        nonlocal state, result
        if state['cho'] is not None:
            if state['jung'] is not None:
                syll = compose_syllable(state['cho'], state['jung'], state['jong'] or "")
                result.append(syll)
            else:
                result.append(state['cho'])
        state = {'cho': None, 'jung': None, 'jong': "", 'jong_combined': False}
    
    i = 0
    N = len(eng_text)
    while i < N:
        # 공백 문자면 현재 음절 flush 후 공백 추가
        if eng_text[i] == ' ':
            flush()
            result.append(' ')
            i += 1
            continue

        token = None
        # 두 글자 조합(예: "hk", "nj" 등)으로 된 모음 먼저 처리
        if i + 1 < N and eng_text[i:i+2] in VOWEL_MAP:
            token = VOWEL_MAP[eng_text[i:i+2]]
            i += 2
        else:
            ch = eng_text[i]
            if ch in VOWEL_MAP:
                token = VOWEL_MAP[ch]
            elif ch in CONSONANT_MAP:
                token = CONSONANT_MAP[ch]
            else:
                flush()
                result.append(ch)
                i += 1
                continue
            i += 1

        if token in JUNGSUNG_LIST:
            if state['cho'] is None:
                # 중성이 들어왔는데 초성이 없으면 기본 초성 'ㅇ' 사용
                state['cho'] = 'ㅇ'
                state['jung'] = token
            elif state['jung'] is None:
                state['jung'] = token
            elif state['jong']:
                # ★ 최종 자음이 있으면 우선 flush하여 최종 자음을 새 음절의 초성으로 이동
                temp = state['jong']
                syll = compose_syllable(state['cho'], state['jung'], "")
                result.append(syll)
                state = {'cho': temp, 'jung': token, 'jong': "", 'jong_combined': False}
            elif (state['jung'], token) in VOWEL_COMBO:
                state['jung'] = VOWEL_COMBO[(state['jung'], token)]
            else:
                syll = compose_syllable(state['cho'], state['jung'], "")
                result.append(syll)
                state = {'cho': 'ㅇ', 'jung': token, 'jong': "", 'jong_combined': False}
        else:  # token이 자음인 경우
            if state['cho'] is None:
                state['cho'] = token
            elif state['jung'] is None:
                if allowDoubleConsonant and (state['cho'], token) in DOUBLE_INITIAL_MAP:
                    state['cho'] = DOUBLE_INITIAL_MAP[(state['cho'], token)]
                else:
                    flush()
                    state['cho'] = token
            else:
                if not state['jong']:
                    state['jong'] = token
                    state['jong_combined'] = False
                else:
                    if (state['jong'], token) in COMPOUND_FINAL_MAP:
                        state['jong'] = COMPOUND_FINAL_MAP[(state['jong'], token)]
                        state['jong_combined'] = True
                    else:
                        flush()
                        state['cho'] = token
    flush()
    return "".join(result)

def koen(kor_text):
    """
    한글(자판 입력값)을 영문 키보드 입력값으로 변환합니다.
    
    :param kor_text: 변환할 한글 문자열
    :return: 영문 키보드 입력 문자열
    """
    result = []
    for ch in kor_text:
        # 공백은 그대로 추가
        if ch == ' ':
            result.append(ch)
            continue
        # 단독 자모이면 바로 매핑 처리
        if ch in CONSONANT_RMAP:
            result.append(CONSONANT_RMAP[ch])
            continue
        if ch in VOWEL_RMAP:
            result.append(VOWEL_RMAP[ch])
            continue
        # 완성형 한글 음절이면 분해하여 매핑
        if is_hangul(ch):
            code = ord(ch)
            syl_index = code - 0xAC00
            cho_index = syl_index // (21 * 28)
            jung_index = (syl_index % (21 * 28)) // 28
            jong_index = syl_index % 28
            cho = CHOSUNG_LIST[cho_index]
            jung = JUNGSUNG_LIST[jung_index]
            eng = CONSONANT_RMAP.get(cho, cho) + VOWEL_RMAP.get(jung, jung)
            if jong_index:
                jong = JONGSUNG_LIST[jong_index]
                if jong in COMPOUND_FINAL_DECOMP:
                    for part in COMPOUND_FINAL_DECOMP[jong]:
                        eng += CONSONANT_RMAP.get(part, part)
                else:
                    eng += CONSONANT_RMAP.get(jong, jong)
            result.append(eng)
        else:
            result.append(ch)
    return "".join(result)

def autofix(text, allowDoubleConsonant=False):
    """
    입력 문자열의 각 구간(한글, 영문, 기타)을 분리하여
    한글인 부분은 koen, 영문인 부분은 enko를 적용합니다.
    
    :param text: 변환할 문자열
    :param allowDoubleConsonant: 두 개의 초성 허용 여부
    :return: 변환된 문자열
    """
    result = []
    current_segment = ""
    current_type = None  # 'hangul', 'roman', 'other'
    
    def flush_segment(seg, seg_type):
        if not seg:
            return ""
        if seg_type == 'hangul':
            return koen(seg)
        elif seg_type == 'roman':
            return enko(seg, allowDoubleConsonant=allowDoubleConsonant)
        else:
            return seg
    
    for ch in text:
        # 한글 여부 판단: 단일 문자에 대해 is_hangul() 사용
        if is_hangul(ch):
            ch_type = 'hangul'
        elif ch.isalpha() and ch.lower() in "abcdefghijklmnopqrstuvwxyz":
            ch_type = 'roman'
        else:
            ch_type = 'other'
        
        if current_type is None:
            current_type = ch_type
            current_segment = ch
        elif ch_type == current_type:
            current_segment += ch
        else:
            result.append(flush_segment(current_segment, current_type))
            current_segment = ch
            current_type = ch_type
    result.append(flush_segment(current_segment, current_type))
    return "".join(result)
