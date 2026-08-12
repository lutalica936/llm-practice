import json
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from document_summarizer import read_text_file, summarize_document


FIXTURE_DIR = PROJECT_ROOT / "tests" / "fixtures"
RESULT_DIR = PROJECT_ROOT / "evaluation"
RESULT_FILE = RESULT_DIR / "results.json"

PROMPT_VERSIONS = ["v1", "v2", "v3"]


def main():
    RESULT_DIR.mkdir(parents=True, exist_ok=True)

    input_files = sorted(FIXTURE_DIR.glob("*.txt"))

    if len(input_files) < 5:
        raise SystemExit(
            f"测试样例不足：当前只有 {len(input_files)} 份，至少需要 5 份"
        )

    rows = []

    for prompt_version in PROMPT_VERSIONS:
        for input_file in input_files[:5]:
            print(
                f"正在测试：{prompt_version} / "
                f"{input_file.name}"
            )

            document = read_text_file(input_file)
            started_at = time.perf_counter()

            try:
                raw_text, result = summarize_document(
                    document=document,
                    prompt_version=prompt_version,
                )

                elapsed_seconds = (
                    time.perf_counter() - started_at
                )

                rows.append({
                    "prompt_version": prompt_version,
                    "input_file": input_file.name,
                    "input_chars": len(document),
                    "parse_success": True,
                    "elapsed_seconds": round(
                        elapsed_seconds,
                        2,
                    ),
                    "usage": "N/A",
                    "error": None,
                    "summary": result.summary,
                    "actions_count": len(result.actions),
                    "questions_count": len(result.questions),
                })

                print("  结果：成功")

            except Exception as error:
                elapsed_seconds = (
                    time.perf_counter() - started_at
                )

                rows.append({
                    "prompt_version": prompt_version,
                    "input_file": input_file.name,
                    "input_chars": len(document),
                    "parse_success": False,
                    "elapsed_seconds": round(
                        elapsed_seconds,
                        2,
                    ),
                    "usage": "N/A",
                    "error": f"{type(error).__name__}: {error}",
                    "summary": None,
                    "actions_count": None,
                    "questions_count": None,
                })

                print(f"  结果：失败，原因：{error}")

    RESULT_FILE.write_text(
        json.dumps(
            rows,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    total = len(rows)
    success = sum(
        1 for row in rows
        if row["parse_success"]
    )

    print("\n===== 评测完成 =====")
    print(f"总测试数：{total}")
    print(f"成功数：{success}")
    print(f"失败数：{total - success}")
    print(f"解析成功率：{success / total:.1%}")
    print(f"结果文件：{RESULT_FILE}")


if __name__ == "__main__":
    main()
