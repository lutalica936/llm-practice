import argparse
from pathlib import Path


def read_text_file(file_path: Path) -> str:
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在：{file_path}")

    if file_path.suffix.lower() != ".txt":
        raise ValueError("当前版本只支持 TXT 文件")

    content = file_path.read_text(encoding="utf-8").strip()

    if not content:
        raise ValueError("输入文件为空")

    return content


def main() -> None:
    parser = argparse.ArgumentParser(
        description="将中文文档整理为摘要、行动项和待确认问题"
    )
    parser.add_argument(
        "input_file",
        type=Path,
        help="UTF-8 编码的 TXT 文件",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="可选的结果保存路径",
    )

    args = parser.parse_args()

    try:
        content = read_text_file(args.input_file)
    except (FileNotFoundError, ValueError, UnicodeDecodeError) as error:
        parser.error(str(error))

    print(f"成功读取：{args.input_file}")
    print(f"字符数：{len(content)}")
    print("项目骨架正常，LLM 摘要功能将在下一步实现。")


if __name__ == "__main__":
    main()
