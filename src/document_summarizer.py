"""文档结构化命令行工具。"""

import argparse
import json
from pathlib import Path
from typing import Optional

from pydantic import ValidationError

from llm_client import request_document_summary
from schemas import DocumentResult


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROMPT_FILE = (
    PROJECT_ROOT
    / "prompts"
    / "document_summarizer_v1.txt"
)
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "output"


def read_text_file(file_path: Path) -> str:
    """读取并检查 TXT 文件。"""

    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在：{file_path}")

    if not file_path.is_file():
        raise ValueError(f"输入路径不是文件：{file_path}")

    if file_path.suffix.lower() != ".txt":
        raise ValueError("当前版本只支持 TXT 文件")

    content = file_path.read_text(
        encoding="utf-8"
    ).strip()

    if not content:
        raise ValueError("输入文件为空")

    return content


def read_prompt() -> str:
    """读取 Prompt v1。"""

    if not PROMPT_FILE.exists():
        raise FileNotFoundError(
            f"找不到提示词文件：{PROMPT_FILE}"
        )

    prompt = PROMPT_FILE.read_text(
        encoding="utf-8"
    ).strip()

    if not prompt:
        raise ValueError("提示词文件为空")

    return prompt


def parse_model_result(
    raw_text: str,
) -> DocumentResult:
    """解析 JSON，并使用 Pydantic 检查结构。"""

    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as error:
        raise ValueError(
            "模型返回的内容不是合法 JSON："
            f"第 {error.lineno} 行，"
            f"第 {error.colno} 列解析失败"
        ) from error

    try:
        return DocumentResult.model_validate(data)
    except ValidationError as error:
        raise ValueError(
            "JSON 可以解析，但数据结构不符合要求："
            f"\n{error}"
        ) from error


def is_json_mode_unsupported(
    error: Exception,
) -> bool:
    """判断错误是否可能由 JSON mode 不兼容导致。"""

    error_message = str(error).lower()

    markers = [
        "response_format",
        "unsupported",
        "not supported",
        "unknown parameter",
    ]

    return any(
        marker in error_message
        for marker in markers
    )


def summarize_document(
    document: str,
) -> tuple[str, DocumentResult]:
    """调用模型并返回原始结果和校验结果。"""

    prompt = read_prompt()

    try:
        raw_text = request_document_summary(
            system_prompt=prompt,
            document=document,
            use_json_mode=True,
        )

    except Exception as error:
        if not is_json_mode_unsupported(error):
            raise

        print(
            "提示：当前接口可能不支持 JSON mode，"
            "正在改用 Prompt 约束方式重试。"
        )

        raw_text = request_document_summary(
            system_prompt=prompt,
            document=document,
            use_json_mode=False,
        )

    parsed_result = parse_model_result(raw_text)

    return raw_text, parsed_result


def save_results(
    input_file: Path,
    raw_text: str,
    result: DocumentResult,
    output_path: Optional[Path],
) -> tuple[Path, Path]:
    """保存模型原始结果和校验后的 JSON。"""

    DEFAULT_OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    raw_output_path = (
        DEFAULT_OUTPUT_DIR
        / f"{input_file.stem}_raw.txt"
    )

    if output_path is None:
        parsed_output_path = (
            DEFAULT_OUTPUT_DIR
            / f"{input_file.stem}_parsed.json"
        )
    else:
        parsed_output_path = output_path

        if parsed_output_path.suffix.lower() != ".json":
            raise ValueError(
                "--output 路径必须以 .json 结尾"
            )

        parsed_output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    raw_output_path.write_text(
        raw_text,
        encoding="utf-8",
    )

    parsed_output_path.write_text(
        json.dumps(
            result.model_dump(),
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    return raw_output_path, parsed_output_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "将中文文档整理为摘要、"
            "行动项和待确认问题"
        )
    )

    parser.add_argument(
        "input_file",
        type=Path,
        help="UTF-8 编码的 TXT 文件",
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="可选的 JSON 结果保存路径",
    )

    args = parser.parse_args()

    try:
        content = read_text_file(
            args.input_file
        )

        print(f"成功读取：{args.input_file}")
        print(f"字符数：{len(content)}")
        print("正在调用模型，请稍候……")

        raw_text, result = summarize_document(
            content
        )

        raw_path, parsed_path = save_results(
            input_file=args.input_file,
            raw_text=raw_text,
            result=result,
            output_path=args.output,
        )

    except (
        FileNotFoundError,
        UnicodeDecodeError,
        ValueError,
    ) as error:
        parser.error(str(error))

    except Exception as error:
        print("文档处理失败。")
        print(f"错误类型：{type(error).__name__}")
        print(f"错误信息：{error}")
        raise SystemExit(1)

    print("\n处理成功。")
    print(f"摘要：{result.summary}")

    print("\n行动项：")
    if result.actions:
        for index, action in enumerate(
            result.actions,
            start=1,
        ):
            print(f"{index}. {action}")
    else:
        print("无")

    print("\n待确认问题：")
    if result.questions:
        for index, question in enumerate(
            result.questions,
            start=1,
        ):
            print(f"{index}. {question}")
    else:
        print("无")

    print(f"\n模型原始结果：{raw_path}")
    print(f"结构化结果：{parsed_path}")


if __name__ == "__main__":
    main()