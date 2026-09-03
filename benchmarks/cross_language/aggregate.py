from __future__ import annotations

import json
import platform
from collections import defaultdict
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
RESULT_DIR = HERE / "results"
OUTPUT_PATH = RESULT_DIR / "benchmark.md"

FEATURE_LABELS = {
    "decompose_text": "텍스트 자모 분해",
    "compose_text": "텍스트 자모 조합",
    "compose_character": "단일 음절 조합",
    "combine_vowels": "겹모음 조합",
    "remove_last_character": "마지막 타건 제거",
    "get_choseong": "초성 추출",
    "has_batchim": "받침 판정",
    "josa_hangul": "조사 선택 - 한글",
    "josa_ascii_acronym": "조사 선택 - 영문 약어",
    "standardize_pronunciation": "표준 발음 변환",
    "romanize": "로마자 표기",
    "number_to_hangul": "숫자 한글 변환",
    "number_to_hangul_mixed": "숫자 혼합 표기",
    "susa": "순우리말 수사",
    "days": "날짜 수사",
    "qwerty_to_hangul": "QWERTY → 한글",
    "hangul_to_qwerty": "한글 → QWERTY",
    "hangul_contains": "부분 음절 검색",
}


def load_results(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def format_ns(value: float) -> str:
    if value < 1_000:
        return f"{value:.1f} ns"
    if value < 1_000_000:
        return f"{value / 1_000:.2f} µs"
    return f"{value / 1_000_000:.2f} ms"


def main() -> None:
    payloads = [
        load_results(RESULT_DIR / "python.json"),
        load_results(RESULT_DIR / "node.json"),
    ]

    rows: list[dict[str, Any]] = []
    runtimes: list[dict[str, Any]] = []
    for payload in payloads:
        runtimes.append(payload["runtime"])
        rows.extend(payload["results"])

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["feature"]].append(row)

    lines: list[str] = []
    lines.append("# hangulpy 기능별 크로스 언어 벤치마크")
    lines.append("")
    lines.append("## 실행 환경")
    lines.append("")
    lines.append(f"- OS: {platform.platform()}")
    for runtime in runtimes:
        lines.append(f"- {runtime['language']}: {runtime['version']}")
    lines.append("")
    lines.append("## 측정 방법")
    lines.append("")
    lines.append("- 각 구현은 같은 GitHub Actions 러너의 한 작업 안에서 순차 실행했습니다.")
    lines.append("- Python은 5회, JavaScript는 20회 워밍업한 뒤 샘플 시간이 약 30 ms 이상이 되도록 반복 횟수를 자동 보정했습니다.")
    lines.append("- 각 항목은 9개 샘플의 중앙값을 사용합니다.")
    lines.append("- 문자열 연산은 문자 또는 자모 1개당 시간, 배치 연산은 단어·숫자·쿼리 1개당 시간으로 정규화했습니다.")
    lines.append("- 비교 라이브러리가 같은 의미를 제공하는 입력만 포함했고, 대표 입력에 대한 결과 일치 검사를 시간 측정 전에 수행했습니다.")
    lines.append("- 낮을수록 빠릅니다. `hangulpy 대비`가 0.50x라면 hangulpy 시간의 절반, 즉 약 2배 빠른 것입니다.")
    lines.append("")

    feature_order = list(FEATURE_LABELS)
    for feature in feature_order:
        candidates = grouped.get(feature, [])
        if not candidates:
            continue

        candidates.sort(key=lambda item: float(item["median_ns_per_unit"]))
        baseline = next((item for item in candidates if item["library"] == "hangulpy"), None)
        baseline_ns = float(baseline["median_ns_per_unit"]) if baseline else None

        lines.append(f"## {FEATURE_LABELS.get(feature, feature)}")
        lines.append("")
        lines.append("| 순위 | 라이브러리 | 언어 | 버전 | 중앙값 | 단위 | hangulpy 대비 | 비고 |")
        lines.append("| ---: | --- | --- | --- | ---: | --- | ---: | --- |")

        for rank, item in enumerate(candidates, start=1):
            current_ns = float(item["median_ns_per_unit"])
            if baseline_ns is None:
                ratio = "-"
            else:
                ratio = f"{current_ns / baseline_ns:.2f}x"
            notes = str(item.get("notes", "")).replace("|", "\\|")
            lines.append(
                "| "
                f"{rank} | {item['library']} | {item['language']} | {item['version']} | "
                f"{format_ns(current_ns)} | {item['unit']} | {ratio} | {notes} |"
            )
        lines.append("")

    lines.append("## 해석 시 주의점")
    lines.append("")
    lines.append("- 언어 런타임 자체의 비용까지 포함한 실제 라이브러리 호출 비용 비교입니다. Python과 V8의 실행 모델 차이는 결과의 일부입니다.")
    lines.append("- JIT 기반 JavaScript는 워밍업 후 정상 상태 성능을 측정합니다. 짧은 CLI의 최초 호출 지연은 별도 지표가 아닙니다.")
    lines.append("- 기능이 비슷해도 예외 처리, Unicode 범위, 숫자·영문 약어 지원 범위가 다른 경우가 있으므로 속도만으로 API 품질을 판단하면 안 됩니다.")
    lines.append("- 현재 1차 러닝은 직접 대응 가능한 공개 API 중심입니다. 퍼지 거리, 한자 분할, 고급 로마자 모드처럼 동등한 경쟁 API가 없는 기능은 순위에서 제외했습니다.")
    lines.append("")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(OUTPUT_PATH.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
