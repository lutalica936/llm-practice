import json
import os
from typing import Any, Dict, List, TypedDict

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv(override=True)

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")
model = os.getenv("OPENAI_MODEL")

if not api_key:
    raise ValueError("没有读取到 OPENAI_API_KEY，请检查 .env 文件")

if not base_url:
    raise ValueError("没有读取到 OPENAI_BASE_URL，请检查 .env 文件")

if not model:
    raise ValueError("没有读取到 OPENAI_MODEL，请检查 .env 文件")


client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)


class AnalysisResult(TypedDict):
    sentiment: str
    keywords: List[str]
    summary: str


SYSTEM_PROMPT = """
你是一名中文文本分析助手。

请分析用户提供的中文文本，并返回一个合法的 JSON 对象。

JSON 必须严格包含以下三个字段：
1. sentiment：字符串，只能是“正面”“中性”或“负面”
2. keywords：字符串数组，提取 3～5 个关键词
3. summary：字符串，用一句简洁的中文概括文本

必须遵守以下要求：
- 只返回 JSON
- 不要返回分析过程
- 不要返回任何额外说明
- 不要使用 Markdown 代码块
- 不要在 JSON 前后添加其他文字
- 所有字段都必须存在

返回格式示例：
{
  "sentiment": "正面",
  "keywords": ["关键词1", "关键词2", "关键词3"],
  "summary": "这里是文本摘要。"
}
""".strip()


def validate_result(data: Dict[str, Any]) -> AnalysisResult:
    """检查解析后的数据是否符合要求。"""

    required_keys = {"sentiment", "keywords", "summary"}

    if set(data.keys()) != required_keys:
        raise ValueError(
            f"字段不正确，期望字段为 {required_keys}，"
            f"实际字段为 {set(data.keys())}"
        )

    if data["sentiment"] not in {"正面", "中性", "负面"}:
        raise ValueError(
            f"sentiment取值不正确：{data['sentiment']}"
        )

    if not isinstance(data["keywords"], list):
        raise ValueError("keywords必须是列表")

    if not 3 <= len(data["keywords"]) <= 5:
        raise ValueError("keywords必须包含3～5个关键词")

    if not all(isinstance(keyword, str) for keyword in data["keywords"]):
        raise ValueError("keywords中的每个关键词都必须是字符串")

    if not isinstance(data["summary"], str):
        raise ValueError("summary必须是字符串")

    if not data["summary"].strip():
        raise ValueError("summary不能为空")

    return {
        "sentiment": data["sentiment"],
        "keywords": data["keywords"],
        "summary": data["summary"],
    }


def analyze_text(text: str) -> AnalysisResult:
    """调用LLM分析文本，并返回经过验证的字典。"""

    if not text.strip():
        raise ValueError("待分析文本不能为空")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": f"请分析以下文本：\n\n{text}",
            },
        ],
        temperature=0,
        max_tokens=500,
        response_format={"type": "json_object"},
    )

    raw_content = response.choices[0].message.content

    if raw_content is None:
        raise ValueError("模型没有返回文本内容")

    try:
        parsed_data = json.loads(raw_content)
    except json.JSONDecodeError as error:
        print("\n模型原始返回内容：")
        print(raw_content)
        raise ValueError(f"模型返回的内容不是合法JSON：{error}") from error

    if not isinstance(parsed_data, dict):
        raise ValueError("模型返回的JSON顶层必须是对象")

    return validate_result(parsed_data)


def main() -> None:
    print("中文文本分析工具")
    text = input("请输入需要分析的中文文本：\n").strip()

    try:
        result = analyze_text(text)
    except ValueError as error:
        print(f"\n分析失败：{error}")
        return

    print("\n分析成功：")
    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        )
    )

    print("\n单独读取字段：")
    print(f"情感：{result['sentiment']}")
    print(f"关键词：{'、'.join(result['keywords'])}")
    print(f"摘要：{result['summary']}")


if __name__ == "__main__":
    main()
