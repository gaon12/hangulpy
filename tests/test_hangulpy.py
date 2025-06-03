import unittest

import hangulpy

class TestHangulPy(unittest.TestCase):
    def test_get_chosung_string(self):
        self.assertEqual(hangulpy.get_chosung_string("가"), "ㄱ")
        text = "대한 사람 대한으로 길이 보전하세"
        self.assertEqual(
            hangulpy.get_chosung_string(text),
            "ㄷㅎㅅㄹㄷㅎㅇㄹㄱㅇㅂㅈㅎㅅ"
        )
        self.assertEqual(
            hangulpy.get_chosung_string(text, keep_spaces=True),
            "ㄷㅎ ㅅㄹ ㄷㅎㅇㄹ ㄱㅇ ㅂㅈㅎㅅ"
        )

    def test_chosung_includes(self):
        self.assertTrue(hangulpy.chosungIncludes("라면", "ㄹㅁ"))
        self.assertFalse(hangulpy.chosungIncludes("라면", "ㄱㅁ"))

    def test_josa(self):
        self.assertEqual(hangulpy.josa("사과", "을/를"), "사과를")
        self.assertEqual(hangulpy.josa("바나나", "이/가"), "바나나가")

    def test_jarip_noun(self):
        self.assertEqual(hangulpy.jarip_noun("확", "율/률"), "확률")
        self.assertEqual(hangulpy.jarip_noun("범", "예/례"), "범례")

    def test_ends_with_consonant(self):
        self.assertTrue(hangulpy.ends_with_consonant("강"))
        self.assertTrue(hangulpy.ends_with_consonant("각"))
        self.assertTrue(hangulpy.ends_with_consonant("ㄱ"))
        self.assertFalse(hangulpy.ends_with_consonant("ㅏ"))

    def test_number_conversion(self):
        self.assertEqual(hangulpy.number_to_hangul(1234), "천이백삼십사")
        self.assertEqual(hangulpy.hangul_to_number("천이백삼십사"), 1234)
        self.assertEqual(hangulpy.number_to_hangul(3.14), "삼 점 일사")
        self.assertAlmostEqual(hangulpy.hangul_to_number("삼점일사"), 3.14, places=2)

    def test_sort_hangul(self):
        words = ["가나", "다라", "나가"]
        self.assertEqual(hangulpy.sort_hangul(words), ["가나", "나가", "다라"])
        self.assertEqual(hangulpy.sort_hangul(words, reverse=True), ["다라", "나가", "가나"])

    def test_is_hangul(self):
        self.assertTrue(hangulpy.is_hangul("가"))
        self.assertFalse(hangulpy.is_hangul("hello"))
        self.assertFalse(hangulpy.is_hangul("안녕 하세요"))
        self.assertTrue(hangulpy.is_hangul("안녕 하세요", spaces=True))

    def test_hangul_contains(self):
        self.assertTrue(hangulpy.hangul_contains("사과", "사"))
        self.assertFalse(hangulpy.hangul_contains("사과", "삽"))
        self.assertTrue(hangulpy.hangul_contains("사과", ""))
        self.assertFalse(hangulpy.hangul_contains("사과", "", notallowempty=True))

    def test_hangul_syllable(self):
        self.assertEqual(hangulpy.hangul_syllable("ㄱ", "ㅏ"), "가")
        self.assertEqual(hangulpy.hangul_syllable("ㄱ", "ㅏ", "ㄱ"), "각")
        with self.assertRaises(Exception):
            hangulpy.hangul_syllable("x", "ㅏ")

if __name__ == "__main__":
    unittest.main()
