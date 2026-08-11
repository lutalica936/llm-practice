"""文档结构化命令行工具。"""

import argparse
import json
from pathlib import Path
from typing import Optional, Tuple

from pydantic import ValidationError

from llm_client import request_document_summary
from schemas import DocumentResult


# 项目根目录：
# /Users/hstsmacbook/Projects/llm-practice
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Prompt 和输出目录
PROMPTS_DIR = PROJECT_ROOT / "prompts"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "output"

# Prompt 版本与文件的对应关系
PROMPT_FILES = {
    "v1": PROMPTS_DIR / "document_summarizer_v1.txt",
    "v2": PROMPTS_DIR / "document_summarizer_v2.txt",
    "v3": PROMPTS_DIR / "document_summarizer_v3.txt",
}


def read_text_file(file_path: Path) -> str:
    """读取并检查 UTF-8 编码的 TXT 文件。"""

    if not file_path.exists():
        raise FileNotFoundError(
            f"文件不存在：{file_path}"
        )

    if not file_path.is_file():
        raise ValueError(
            f"输入路径不是文件：{file_path}"
        )

    if file_path.suffix.lower() != ".txt":
        raise ValueError(
            "当前版本只支持 TXT 文件"
        )

    content = file_path.read_text(
        encoding="utf-8"
    ).strip()

    if not content:
        raise ValueError(
            "输入文件为空"
        )

    return content


def read_prompt(prompt_version: str) -> str:
    """按照版本号读取提示词文件。"""

    if prompt_version not in PROMPT_FILES:
        raise ValueError(
            f"不支持的 Prompt 版本：{prompt_version}"
        )

    prompt_file = PROMPT_FILES[prompt_version]

    if not prompt_file.exists():
        raise FileNotFoundError(
            f"找不到提示词文件：{prompt_file}"
        )

    if not prompt_file.is_file():
        raise ValueError(
            f"提示词路径不是文件：{prompt_file}"
        )

    prompt = prompt_file.read_text(
        encoding="utf-8"
    ).strip()

    if not prompt:
        raise ValueError(
            f"提示词文件为空：{prompt_file}"
        )

    return prompt


def parse_model_result(
    raw_text: str,
) -> DocumentResult:
    """解析模型返回的 JSON，并用 Pydantic 检查结构。"""

    try:
        data = json.loads(raw_text)

    except json.JSONDecodeError as error:
        raise ValueError(
            "模型返回的内容不是合法 JSON："
            f"第 {error.lineno} 行，"
            f"第 {error.colno} 列解析失败"
        ) from error

    try:
        result = DocumentResult.model_validate(
            data
        )

    except ValidationError as error:
        raise ValueError(
            "JSON 可以解析，但数据结构不符合要求："
            f"\n{error}"
        ) from error

    return result


def is_json_mode_unsupported(
    error: Exception,
) -> bool:
    """判断错误是否可能由 JSON mode 不兼容导致。"""

    error_message = str(error).lower()

    unsupported_markers = [
        "response_format",
        "unsupported",
        "not supported",
        "unknown parameter",
    ]

    return any(
        marker in error_message
        for marker in unsupported_markers
    )


def summarize_document(
    document: str,
    prompt_version: str,
) -> Tuple[str, DocumentResult]:
    """
    使用指定版本的 Prompt 处理文档。

    返回：
    1. 模型返回的原始文本；
    2. 经过 JSON 和 Pydantic 校验的结果。
    """

    prompt = read_prompt(
        prompt_version
    )

    try:
        # 首先尝试使用 JSON mode
        raw_text = request_document_summary(
            system_prompt=prompt,
            document=document,
            use_json_mode=True,
        )

    except Exception as error:
        # 只有错误信息明确表明 JSON mode
        # 可能不兼容时，才去掉 response_format 重试。
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

    parsed_result = parse_model_result(
        raw_text
    )

    return raw_text, parsed_result


def save_results(
    input_file: Path,
    raw_text: str,
    result: DocumentResult,
    prompt_version: str,
    output_path: Optional[Path],
) -> Tuple[Path, Path]:
    """
    保存模型原始结果和经过校验的 JSON 结果。

    默认文件名中包含 Prompt 版本，
    防止 v1、v2、v3 的结果相互覆盖。
    """

    DEFAULT_OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # 模型原始返回结果始终保存在默认 output 目录
    raw_output_path = (
        DEFAULT_OUTPUT_DIR
        / (
            f"{input_file.stem}_"
            f"{prompt_version}_raw.txt"
        )
    )

    # 未指定 --output 时，使用默认输出路径
    if output_path is None:
        parsed_output_path = (
            DEFAULT_OUTPUT_DIR
            / (
                f"{input_file.stem}_"
                f"{prompt_version}_parsed.json"
            )
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


def print_result(
    result: DocumentResult,
) -> None:
    """在终端中显示结构化结果。"""

    print("\n处理成功。")

    print("\n摘要：")
    print(result.summary)

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


def main() -> None:
    """解析命令行参数并运行文档结构化流程。"""

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
        "--prompt-version",
        choices=["v1", "v2", "v3"],
        default="v1",
        help=(
            "选择提示词版本："
            "v1、v2 或 v3，默认使用 v1"
        ),
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="可选的 JSON 结果保存路径",
    )

    args = parser.parse_args()

    try:
        # 第一步：读取输入文件
        content = read_text_file(
            args.input_file
        )

        print(
            f"成功读取：{args.input_file}"
        )
        print(
            f"字符数：{len(content)}"
        )
        print(
            f"Prompt 版本：{args.prompt_version}"
        )
        print(
            "正在调用模型，请稍候……"
        )

        # 第二步：调用模型并验证结果
        raw_text, result = summarize_document(
            document=content,
            prompt_version=args.prompt_version,
        )

        # 第三步：保存原始结果和结构化结果
        raw_path, parsed_path = save_results(
            input_file=args.input_file,
            raw_text=raw_text,
            result=result,
            prompt_version=args.prompt_version,
            output_path=args.output,
        )

    except (
        FileNotFoundError,
        UnicodeDecodeError,
        ValueError,
    ) as error:
        # 输入、Prompt、JSON 或 Pydantic
        # 校验错误使用 argparse 的错误格式显示。
        parser.error(
            str(error)
        )

    except Exception as error:
        # API、网络、认证等其他异常
        print("\n文档处理失败。")
        print(
            f"错误类型：{type(error).__name__}"
        )
        print(
            f"错误信息：{error}"
        )
        raise SystemExit(1)

    # 第四步：在终端展示结果
    print_result(
        result
    )

    print(
        f"\n模型原始结果：{raw_path}"
    )
    print(
        f"结构化结果：{parsed_path}"
    )


if __name__ == "__main__":
    main()