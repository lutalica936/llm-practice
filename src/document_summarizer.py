"""文档结构化命令行工具。"""

import argparse
import json
from pathlib import Path
from typing import Optional, Tuple

from pydantic import ValidationError

from llm_client import request_document_summary
from schemas import DocumentResult


# 项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Prompt 和默认输出目录
PROMPTS_DIR = PROJECT_ROOT / "prompts"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "output"

# 当前版本允许输入的最大字符数。
# 这里使用 Python 的 len() 计算字符数，不是 token 数。
MAX_DOCUMENT_CHARS = 12000

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

    try:
        content = file_path.read_text(
            encoding="utf-8"
        ).strip()

    except UnicodeDecodeError as error:
        raise ValueError(
            "无法按 UTF-8 编码读取文件。"
            "请把文件转换为 UTF-8 编码后重试"
        ) from error

    if not content:
        raise ValueError(
            "输入文件为空"
        )

    if len(content) > MAX_DOCUMENT_CHARS:
        raise ValueError(
            f"输入文档过长：当前 {len(content)} 个字符，"
            f"最多支持 {MAX_DOCUMENT_CHARS} 个字符。"
            "请缩短文档或拆分后重试"
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

    try:
        prompt = prompt_file.read_text(
            encoding="utf-8"
        ).strip()

    except UnicodeDecodeError as error:
        raise ValueError(
            f"无法按 UTF-8 编码读取提示词文件：{prompt_file}"
        ) from error

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
        # 首先尝试使用 JSON mode。
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
            "\n提示：当前接口可能不支持 JSON mode，"
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


def render_json(
    result: DocumentResult,
) -> str:
    """把结构化结果转换为格式化 JSON 文本。"""

    return json.dumps(
        result.model_dump(),
        ensure_ascii=False,
        indent=2,
    ) + "\n"


def render_markdown(
    result: DocumentResult,
) -> str:
    """把结构化结果转换为便于阅读的 Markdown 文本。"""

    lines = [
        "# 文档结构化结果",
        "",
        "## 摘要",
        "",
        result.summary,
        "",
        "## 行动项",
        "",
    ]

    if result.actions:
        for index, action in enumerate(
            result.actions,
            start=1,
        ):
            lines.append(
                f"{index}. {action}"
            )
    else:
        lines.append("无")

    lines.extend([
        "",
        "## 待确认问题",
        "",
    ])

    if result.questions:
        for index, question in enumerate(
            result.questions,
            start=1,
        ):
            lines.append(
                f"{index}. {question}"
            )
    else:
        lines.append("无")

    return "\n".join(lines) + "\n"


def get_expected_suffix(
    output_format: str,
) -> str:
    """根据输出格式返回正确的文件扩展名。"""

    if output_format == "json":
        return ".json"

    if output_format == "markdown":
        return ".md"

    raise ValueError(
        f"不支持的输出格式：{output_format}"
    )


def build_output_text(
    result: DocumentResult,
    output_format: str,
) -> str:
    """根据用户选择生成 JSON 或 Markdown 文本。"""

    if output_format == "json":
        return render_json(
            result
        )

    if output_format == "markdown":
        return render_markdown(
            result
        )

    raise ValueError(
        f"不支持的输出格式：{output_format}"
    )


def save_results(
    input_file: Path,
    raw_text: str,
    result: DocumentResult,
    prompt_version: str,
    output_format: str,
    output_path: Optional[Path],
) -> Tuple[Path, Path]:
    """
    保存模型原始结果和最终结果。

    模型的原始返回始终保存为 TXT。
    最终结果可保存为 JSON 或 Markdown。
    """

    DEFAULT_OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # 原始返回固定保存在默认 output 目录。
    raw_output_path = (
        DEFAULT_OUTPUT_DIR
        / (
            f"{input_file.stem}_"
            f"{prompt_version}_raw.txt"
        )
    )

    expected_suffix = get_expected_suffix(
        output_format
    )

    # 没有指定 --output 时，自动生成文件名。
    if output_path is None:
        final_output_path = (
            DEFAULT_OUTPUT_DIR
            / (
                f"{input_file.stem}_"
                f"{prompt_version}"
                f"{expected_suffix}"
            )
        )

    else:
        final_output_path = output_path

        if (
            final_output_path.suffix.lower()
            != expected_suffix
        ):
            raise ValueError(
                f"--format {output_format} 要求 "
                f"--output 路径以 "
                f"{expected_suffix} 结尾"
            )

        # 允许用户指定尚不存在的子目录。
        final_output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    final_text = build_output_text(
        result=result,
        output_format=output_format,
    )

    raw_output_path.write_text(
        raw_text,
        encoding="utf-8",
    )

    final_output_path.write_text(
        final_text,
        encoding="utf-8",
    )

    return raw_output_path, final_output_path


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
            print(
                f"{index}. {action}"
            )
    else:
        print("无")

    print("\n待确认问题：")

    if result.questions:
        for index, question in enumerate(
            result.questions,
            start=1,
        ):
            print(
                f"{index}. {question}"
            )
    else:
        print("无")


def create_argument_parser() -> argparse.ArgumentParser:
    """创建并配置命令行参数解析器。"""

    parser = argparse.ArgumentParser(
        description=(
            "读取中文 TXT 文档，调用 LLM，"
            "整理为摘要、行动项和待确认问题。"
        ),
        epilog=(
            "使用示例：\n"
            "\n"
            "  1. 使用默认设置，输出 JSON：\n"
            "     python src/document_summarizer.py "
            "tests/fixtures/short_note.txt\n"
            "\n"
            "  2. 选择 v3 Prompt 并输出 Markdown：\n"
            "     python src/document_summarizer.py "
            "tests/fixtures/long_report.txt "
            "--prompt-version v3 "
            "--format markdown "
            "--output output/long_report.md\n"
            "\n"
            "  3. 指定 JSON 输出文件：\n"
            "     python src/document_summarizer.py "
            "tests/fixtures/meeting_actions.txt "
            "--format json "
            "--output output/meeting_actions.json"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "input_file",
        type=Path,
        help=(
            "输入文件路径。\n"
            "必须是 UTF-8 编码的 TXT 文件，"
            f"最多 {MAX_DOCUMENT_CHARS} 个字符"
        ),
    )

    parser.add_argument(
        "--prompt-version",
        choices=["v1", "v2", "v3"],
        default="v3",
        help=(
            "选择提示词版本：v1、v2 或 v3。\n"
            "默认值：v3"
        ),
    )

    parser.add_argument(
        "--format",
        dest="output_format",
        choices=["json", "markdown"],
        default="json",
        help=(
            "选择最终结果格式：json 或 markdown。\n"
            "默认值：json"
        ),
    )

    parser.add_argument(
        "--output",
        type=Path,
        help=(
            "可选的结果保存路径。\n"
            "JSON 格式必须以 .json 结尾；"
            "Markdown 格式必须以 .md 结尾。\n"
            "不填写时，结果自动保存在 output/ 目录"
        ),
    )

    return parser


def main() -> None:
    """解析命令行参数并运行文档结构化流程。"""

    parser = create_argument_parser()
    args = parser.parse_args()

    try:
        # 第一步：读取并校验输入文件。
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
            f"输出格式：{args.output_format}"
        )
        print(
            "正在调用模型，请稍候……"
        )

        # 第二步：调用模型并验证结果。
        raw_text, result = summarize_document(
            document=content,
            prompt_version=args.prompt_version,
        )

        # 第三步：保存原始结果和最终结果。
        raw_path, final_path = save_results(
            input_file=args.input_file,
            raw_text=raw_text,
            result=result,
            prompt_version=args.prompt_version,
            output_format=args.output_format,
            output_path=args.output,
        )

    except (
        FileNotFoundError,
        ValueError,
    ) as error:
        # 输入、Prompt、JSON、Pydantic
        # 或输出路径错误。
        #
        # parser.error() 会显示清晰的参数错误，
        # 并以非零退出码 2 结束程序。
        parser.error(
            str(error)
        )

    except Exception as error:
        # API、网络、认证等其他异常。
        print("\n文档处理失败。")
        print(
            f"错误类型：{type(error).__name__}"
        )
        print(
            f"错误信息：{error}"
        )

        # 使用退出码 1 表示程序运行失败。
        raise SystemExit(1)

    # 第四步：在终端展示结果。
    print_result(
        result
    )

    print(
        f"\n模型原始结果：{raw_path}"
    )
    print(
        f"最终结果：{final_path}"
    )


if __name__ == "__main__":
    main()