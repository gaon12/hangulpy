# hangulpy/__init__.py

# Original functions
from .chosung import chosungIncludes, get_chosung_string
from .hangul_check import is_hangul_consonant, is_hangul_vowel
from .hangul_contains import (
    hangul_contains,
    hangul_search,
    hangul_search_all,
    HangulSearcher,
)
from .hangul_decompose import decompose_hangul_string
from .hangul_ends_with_consonant import ends_with_consonant
from .hangul_number import float_to_hangul, hangul_to_number, number_to_hangul
from .hangul_role import can_be_chosung, can_be_jongsung
from .hangul_sort import sort_hangul
from .hangul_split import split_hangul_string
from .hangul_syllable import hangul_syllable
from .hangul_typoerror import koen, enko, autofix
from .is_hangul import is_hangul
from .josa import has_jongsung, josa
from .match_hangul_pattern import match_hangul_pattern
from .noun import jarip_noun

# New enhanced functions
from .hangul_properties import (
    is_complete_hangul,
    is_chosung,
    is_jungsung,
    is_jongsung,
    get_chosung,
    get_jungsung,
    get_jongsung,
    get_hangul_components,
)

from .hangul_assemble import (
    split_syllables,
    join_jamos,
    disassemble,
    assemble,
)

from .romanize import (
    Romanizer,
    romanize,
)

__all__ = [
    # Original exports
    'chosungIncludes',
    'get_chosung_string',
    'is_hangul_consonant',
    'is_hangul_vowel',
    'hangul_contains',
    'decompose_hangul_string',
    'ends_with_consonant',
    'float_to_hangul',
    'hangul_to_number',
    'number_to_hangul',
    'can_be_chosung',
    'can_be_jongsung',
    'sort_hangul',
    'split_hangul_string',
    'hangul_syllable',
    'koen',
    'enko',
    'autofix',
    'is_hangul',
    'has_jongsung',
    'josa',
    'match_hangul_pattern',
    'jarip_noun',
    # New enhanced search functions
    'hangul_search',
    'hangul_search_all',
    'HangulSearcher',
    # New property checking functions
    'is_complete_hangul',
    'is_chosung',
    'is_jungsung',
    'is_jongsung',
    'get_chosung',
    'get_jungsung',
    'get_jongsung',
    'get_hangul_components',
    # New assembly functions
    'split_syllables',
    'join_jamos',
    'disassemble',
    'assemble',
    # Romanization
    'Romanizer',
    'romanize',
]
