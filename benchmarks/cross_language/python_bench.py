from __future__ import annotations

import json
import statistics
import time
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Callable

import hangeul_jamo_py as hangeul_jamo_py
import hangul_jamo
import hgtk
from korean_romanizer import romanize as korean_romanize

import hangulpy
from hangulpy import (
    combine_character,
    combine_vowels,
    convert_hangul_to_qwerty,
    convert_qwerty_to_hangul,
    days,
    extract_chosung,
    hangul_contains,
    has_batchim,
    join_jamos,
    josa,
    number_to_hangul,
    number_to_hangul_mixed,
    remove_last_character,
    romanize,
    split_syllables,
    standardize_pronunciation,
    susa,
)

RESULT_PATH = Path(__file__).with_name("results") / "python.json"

TEXT = (
    "가나다라마바사아자차카타파하 한글 사랑 나라 학교 한국어 사람 대한민국 " * 128
).strip()
JAMO_TEXT = split_syllables(TEXT, output_format="string")
ROMAN_TEXT = ("한글 사랑 나라 학교 한국어 대한민국 " * 96).strip()
PRON_TEXT = ("굳이 같이 국물 신라 독립 앞문 맏형 숱하다 옷한벌 " * 64).strip()
QWERTY_TEXT = ("dkssudgktpdy gksrmf tkfkd eogksalsrnr " * 128).strip()
HANGUL_QWERTY_TEXT = convert_qwerty_to_hangul(QWERTY_TEXT)
WORDS = ["사과", "하늘", "바다", "달", "집", "학교", "사람", "한국"] * 64
ACRONYMS = ["RAM", "API", "CPU", "GPU", "HTML", "URL", "JSON", "SQL"] * 64
NUMBERS = [0, 1, 2, 9, 10, 11, 20, 21, 99, 100, 101, 1004, 12345, 123456780] * 32
SUSA_NUMBERS = list(range(1, 101)) * 4
DAY_NUMBERS = list(range(1, 31)) * 12
SEARCH_CASES = [
    ("달걀", "닭"),
    ("도우미", "도움"),
    ("사과", "삭"),
    ("한글 처리 라이브러리", "ㅎㄱ"),
] * 128

SINK = 0


def package_version(name: str) -> str:
    try:
        return version(name)
    except PackageNotFoundError:
        return "unknown"


def consume(value: object) -> int:
    """Return a tiny checksum so benchmark results are observably consumed."""
    if isinstance(value, str):
        return len(value)
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (tuple, list)):
        return len(value)
    return hash(value) & 0xFFFF


def benchmark(
    *,
    feature: str,
    library: str,
    library_version: str,
    fn: Callable[[], object],
    work_units: int,
    unit: str,
    notes: str = "",
) -> dict[str, object]:
    """Measure a callable with calibration, warm-up, and median sampling."""
    global SINK

    # Warm up import caches, regular-expression caches, and hot code paths.
    for _ in range(5):
        SINK ^= consume(fn())

    # Calibrate each sample to at least roughly 30 ms to reduce timer noise.
    loops = 1
    while True:
        start = time.perf_counter_ns()
        local_sink = 0
        for _ in range(loops):
            local_sink ^= consume(fn())
        elapsed = time.perf_counter_ns() - start
        SINK ^= local_sink
        if elapsed >= 30_000_000 or loops >= 1_048_576:
            break
        loops *= 2

    samples: list[float] = []
    for _ in range(9):
        start = time.perf_counter_ns()
        local_sink = 0
        for _ in range(loops):
            local_sink ^= consume(fn())
        elapsed = time.perf_counter_ns() - start
        SINK ^= local_sink
        samples.append(elapsed / loops / work_units)

    median_ns = statistics.median(samples)
    return {
        "feature": feature,
        "library": library,
        "language": "Python",
        "version": library_version,
        "unit": unit,
        "median_ns_per_unit": round(median_ns, 3),
        "samples": 9,
        "notes": notes,
    }


def main() -> None:
    results: list[dict[str, object]] = []

    hangulpy_version = getattr(hangulpy, "__version__", package_version("hangulpy"))

    # Core text decomposition. The corpus intentionally avoids ambiguous compound
    # compatibility-jamo sequences so every library performs the same operation.
    expected_decomposed = split_syllables(TEXT, output_format="string")
    assert hangeul_jamo_py.decompose_hcj(TEXT) == expected_decomposed
    assert hangul_jamo.decompose(TEXT) == expected_decomposed
    assert hgtk.text.decompose(TEXT, compose_code="") == expected_decomposed

    results.append(
        benchmark(
            feature="decompose_text",
            library="hangulpy",
            library_version=hangulpy_version,
            fn=lambda: split_syllables(TEXT, output_format="string"),
            work_units=len(TEXT),
            unit="char",
        )
    )
    results.append(
        benchmark(
            feature="decompose_text",
            library="hangeul-jamo-py",
            library_version=package_version("hangeul-jamo-py"),
            fn=lambda: hangeul_jamo_py.decompose_hcj(TEXT),
            work_units=len(TEXT),
            unit="char",
        )
    )
    results.append(
        benchmark(
            feature="decompose_text",
            library="hangul-jamo",
            library_version=package_version("hangul-jamo"),
            fn=lambda: hangul_jamo.decompose(TEXT),
            work_units=len(TEXT),
            unit="char",
        )
    )
    results.append(
        benchmark(
            feature="decompose_text",
            library="hgtk",
            library_version=package_version("hgtk"),
            fn=lambda: hgtk.text.decompose(TEXT, compose_code=""),
            work_units=len(TEXT),
            unit="char",
            notes="compose_code disabled for output parity",
        )
    )

    # Core text composition.
    expected_composed = join_jamos(list(JAMO_TEXT))
    assert expected_composed == TEXT
    assert hangeul_jamo_py.compose_hcj(JAMO_TEXT) == TEXT
    assert hangul_jamo.compose(JAMO_TEXT) == TEXT

    results.append(
        benchmark(
            feature="compose_text",
            library="hangulpy",
            library_version=hangulpy_version,
            fn=lambda: join_jamos(list(JAMO_TEXT)),
            work_units=len(JAMO_TEXT),
            unit="jamo",
        )
    )
    results.append(
        benchmark(
            feature="compose_text",
            library="hangeul-jamo-py",
            library_version=package_version("hangeul-jamo-py"),
            fn=lambda: hangeul_jamo_py.compose_hcj(JAMO_TEXT),
            work_units=len(JAMO_TEXT),
            unit="jamo",
        )
    )
    results.append(
        benchmark(
            feature="compose_text",
            library="hangul-jamo",
            library_version=package_version("hangul-jamo"),
            fn=lambda: hangul_jamo.compose(JAMO_TEXT),
            work_units=len(JAMO_TEXT),
            unit="jamo",
        )
    )

    # Single-syllable composition.
    assert combine_character("ㅎ", "ㅏ", "ㄴ") == "한"
    assert hgtk.letter.compose("ㅎ", "ㅏ", "ㄴ") == "한"
    assert hangul_jamo.compose_jamo_characters("ㅎ", "ㅏ", "ㄴ") == "한"
    compose_inputs = [("ㅎ", "ㅏ", "ㄴ"), ("ㄱ", "ㅡ", "ㄹ"), ("ㅅ", "ㅏ", None)] * 256

    results.append(
        benchmark(
            feature="compose_character",
            library="hangulpy",
            library_version=hangulpy_version,
            fn=lambda: [combine_character(a, b, c or "") for a, b, c in compose_inputs],
            work_units=len(compose_inputs),
            unit="syllable",
        )
    )
    results.append(
        benchmark(
            feature="compose_character",
            library="hgtk",
            library_version=package_version("hgtk"),
            fn=lambda: [hgtk.letter.compose(a, b, c or "") for a, b, c in compose_inputs],
            work_units=len(compose_inputs),
            unit="syllable",
        )
    )
    results.append(
        benchmark(
            feature="compose_character",
            library="hangul-jamo",
            library_version=package_version("hangul-jamo"),
            fn=lambda: [hangul_jamo.compose_jamo_characters(a, b, c) for a, b, c in compose_inputs],
            work_units=len(compose_inputs),
            unit="syllable",
        )
    )

    # Direct es-hangul-compatible API surface, measured here for hangulpy.
    vowel_pairs = [("ㅗ", "ㅏ"), ("ㅗ", "ㅐ"), ("ㅜ", "ㅓ"), ("ㅡ", "ㅣ")] * 256
    results.append(
        benchmark(
            feature="combine_vowels",
            library="hangulpy",
            library_version=hangulpy_version,
            fn=lambda: [combine_vowels(a, b) for a, b in vowel_pairs],
            work_units=len(vowel_pairs),
            unit="pair",
        )
    )

    edit_words = ["감", "값", "한글", "전화", "사과"] * 256
    results.append(
        benchmark(
            feature="remove_last_character",
            library="hangulpy",
            library_version=hangulpy_version,
            fn=lambda: [remove_last_character(word) for word in edit_words],
            work_units=len(edit_words),
            unit="word",
        )
    )

    results.append(
        benchmark(
            feature="get_choseong",
            library="hangulpy",
            library_version=hangulpy_version,
            fn=lambda: extract_chosung(TEXT),
            work_units=len(TEXT),
            unit="char",
        )
    )

    assert has_batchim("한") is True and hgtk.checker.has_batchim("한") is True
    assert has_batchim("하") is False and hgtk.checker.has_batchim("하") is False
    results.append(
        benchmark(
            feature="has_batchim",
            library="hangulpy",
            library_version=hangulpy_version,
            fn=lambda: [has_batchim(word) for word in WORDS],
            work_units=len(WORDS),
            unit="word",
        )
    )
    results.append(
        benchmark(
            feature="has_batchim",
            library="hgtk",
            library_version=package_version("hgtk"),
            fn=lambda: [hgtk.checker.has_batchim(word) for word in WORDS],
            work_units=len(WORDS),
            unit="word",
        )
    )

    assert josa("하늘", "은/는") == hgtk.josa.attach("하늘", hgtk.josa.EUN_NEUN)
    assert josa("바다", "은/는") == hgtk.josa.attach("바다", hgtk.josa.EUN_NEUN)
    results.append(
        benchmark(
            feature="josa_hangul",
            library="hangulpy",
            library_version=hangulpy_version,
            fn=lambda: [josa(word, "은/는") for word in WORDS],
            work_units=len(WORDS),
            unit="word",
        )
    )
    results.append(
        benchmark(
            feature="josa_hangul",
            library="hgtk",
            library_version=package_version("hgtk"),
            fn=lambda: [hgtk.josa.attach(word, hgtk.josa.EUN_NEUN) for word in WORDS],
            work_units=len(WORDS),
            unit="word",
        )
    )
    results.append(
        benchmark(
            feature="josa_ascii_acronym",
            library="hangulpy",
            library_version=hangulpy_version,
            fn=lambda: [josa(word, "은/는") for word in ACRONYMS],
            work_units=len(ACRONYMS),
            unit="word",
        )
    )

    # Pronunciation and romanization.
    assert romanize("한글") == korean_romanize("한글") == "hangeul"
    results.append(
        benchmark(
            feature="standardize_pronunciation",
            library="hangulpy",
            library_version=hangulpy_version,
            fn=lambda: standardize_pronunciation(PRON_TEXT),
            work_units=len(PRON_TEXT),
            unit="char",
        )
    )
    results.append(
        benchmark(
            feature="romanize",
            library="hangulpy",
            library_version=hangulpy_version,
            fn=lambda: romanize(ROMAN_TEXT),
            work_units=len(ROMAN_TEXT),
            unit="char",
        )
    )
    results.append(
        benchmark(
            feature="romanize",
            library="korean-romanizer",
            library_version=package_version("korean-romanizer"),
            fn=lambda: korean_romanize(ROMAN_TEXT),
            work_units=len(ROMAN_TEXT),
            unit="char",
        )
    )

    # Number and native-Korean number helpers.
    results.append(
        benchmark(
            feature="number_to_hangul",
            library="hangulpy",
            library_version=hangulpy_version,
            fn=lambda: [number_to_hangul(value) for value in NUMBERS],
            work_units=len(NUMBERS),
            unit="number",
        )
    )
    results.append(
        benchmark(
            feature="number_to_hangul_mixed",
            library="hangulpy",
            library_version=hangulpy_version,
            fn=lambda: [number_to_hangul_mixed(value) for value in NUMBERS],
            work_units=len(NUMBERS),
            unit="number",
        )
    )
    results.append(
        benchmark(
            feature="susa",
            library="hangulpy",
            library_version=hangulpy_version,
            fn=lambda: [susa(value) for value in SUSA_NUMBERS],
            work_units=len(SUSA_NUMBERS),
            unit="number",
        )
    )
    results.append(
        benchmark(
            feature="days",
            library="hangulpy",
            library_version=hangulpy_version,
            fn=lambda: [days(value) for value in DAY_NUMBERS],
            work_units=len(DAY_NUMBERS),
            unit="number",
        )
    )

    # Keyboard conversion.
    results.append(
        benchmark(
            feature="qwerty_to_hangul",
            library="hangulpy",
            library_version=hangulpy_version,
            fn=lambda: convert_qwerty_to_hangul(QWERTY_TEXT),
            work_units=len(QWERTY_TEXT),
            unit="char",
        )
    )
    results.append(
        benchmark(
            feature="hangul_to_qwerty",
            library="hangulpy",
            library_version=hangulpy_version,
            fn=lambda: convert_hangul_to_qwerty(HANGUL_QWERTY_TEXT),
            work_units=len(HANGUL_QWERTY_TEXT),
            unit="char",
        )
    )

    # Partial-syllable search, comparable with Hangul.js search semantics on the
    # selected canonical cases.
    assert hangul_contains("달걀", "닭") is True
    assert hangul_contains("도우미", "도움") is True
    assert hangul_contains("사과", "삭") is True
    results.append(
        benchmark(
            feature="hangul_contains",
            library="hangulpy",
            library_version=hangulpy_version,
            fn=lambda: [hangul_contains(text, query) for text, query in SEARCH_CASES],
            work_units=len(SEARCH_CASES),
            unit="query",
        )
    )

    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(
        json.dumps(
            {
                "runtime": {
                    "language": "Python",
                    "version": __import__("sys").version.split()[0],
                    "sink": SINK,
                },
                "results": results,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"wrote {len(results)} Python benchmark rows to {RESULT_PATH}")


if __name__ == "__main__":
    main()
