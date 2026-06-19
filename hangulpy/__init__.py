# hangulpy/__init__.py

# Original functions
from .chosung import chosungIncludes, get_chosung_string
from .hangul_assemble import (
    assemble,
    combine_character,
    combine_vowels,
    disassemble,
    disassemble_complete_character,
    disassemble_to_groups,
    join_jamos,
    remove_last_character,
    split_syllables,
)
from .hangul_check import is_hangul_consonant, is_hangul_vowel
from .hangul_contains import (
    HangulSearcher,
    hangul_contains,
    hangul_search,
    hangul_search_all,
)
from .hangul_decompose import decompose_hangul_string
from .hangul_ends_with_consonant import ends_with_consonant
from .hangul_number import (
    amount_to_hangul,
    days,
    float_to_hangul,
    hangul_to_number,
    number_to_hangul,
    number_to_hangul_mixed,
    seosusa,
    susa,
)

# New enhanced functions
from .hangul_properties import (
    get_chosung,
    get_hangul_components,
    get_jongsung,
    get_jungsung,
    is_chosung,
    is_complete_hangul,
    is_jongsung,
    is_jungsung,
)
from .hangul_role import can_be_chosung, can_be_jongsung
from .hangul_sort import sort_hangul
from .hangul_split import split_hangul_string
from .hangul_syllable import hangul_syllable
from .hangul_typoerror import (
    autofix,
    convert_hangul_to_qwerty,
    convert_qwerty_to_alphabet,
    convert_qwerty_to_hangul,
    enko,
    koen,
)
from .is_hangul import is_hangul
from .josa import has_jongsung, josa, josa_pick
from .match_hangul_pattern import match_hangul_pattern
from .noun import jarip_noun
from .romanize import (
    Romanizer,
    romanize,
)

__all__ = [
    # Original exports
    "chosungIncludes",
    "get_chosung_string",
    "is_hangul_consonant",
    "is_hangul_vowel",
    "hangul_contains",
    "decompose_hangul_string",
    "ends_with_consonant",
    "float_to_hangul",
    "hangul_to_number",
    "number_to_hangul",
    "number_to_hangul_mixed",
    "amount_to_hangul",
    "susa",
    "seosusa",
    "days",
    "can_be_chosung",
    "can_be_jongsung",
    "sort_hangul",
    "split_hangul_string",
    "hangul_syllable",
    "koen",
    "enko",
    "autofix",
    "convert_hangul_to_qwerty",
    "convert_qwerty_to_hangul",
    "convert_qwerty_to_alphabet",
    "is_hangul",
    "has_jongsung",
    "josa",
    "josa_pick",
    "match_hangul_pattern",
    "jarip_noun",
    # New enhanced search functions
    "hangul_search",
    "hangul_search_all",
    "HangulSearcher",
    # New property checking functions
    "is_complete_hangul",
    "is_chosung",
    "is_jungsung",
    "is_jongsung",
    "get_chosung",
    "get_jungsung",
    "get_jongsung",
    "get_hangul_components",
    # New assembly functions
    "split_syllables",
    "join_jamos",
    "disassemble",
    "assemble",
    "combine_vowels",
    "combine_character",
    "disassemble_to_groups",
    "disassemble_complete_character",
    "remove_last_character",
    # Romanization
    "Romanizer",
    "romanize",
]
