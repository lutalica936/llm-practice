import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

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


STYLE_PROMPTS = {
    "1": """
你是一名严谨的中英翻译。
请采用直译风格，尽量保留原文的句式、信息和表达顺序。
不要解释，不要添加原文不存在的信息，只输出译文。
""",
    "2": """
你是一名专业的中英翻译。
请采用意译风格，在准确保留原意的前提下，使译文自然、流畅，
符合目标语言的表达习惯。
不要解释，只输出译文。
""",
    "3": """
你是一名擅长日常交流的中英翻译。
请采用口语化风格，使译文听起来自然、轻松，适合日常对话。
不要解释，只输出译文。
""",
}


def translate(text: str, style: str) -> str:
    """根据指定风格翻译中英文文本。"""

    system_prompt = STYLE_PROMPTS.get(style)

    if system_prompt is None:
        raise ValueError("翻译风格必须是 1、2 或 3")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt.strip(),
            },
            {
                "role": "user",
                "content": (
                    "请自动判断下面文本的语言："
                    "如果是中文就翻译成英文，如果是英文就翻译成中文。\n\n"
                    f"待翻译文本：\n{text}"
                ),
            },
        ],
        temperature=0.2,
        max_tokens=500,
    )

    result = response.choices[0].message.content

    if result is None:
        raise ValueError("模型没有返回文本内容")

    return result.strip()


def main() -> None:
    print("中英翻译工具")
    print("1. 直译")
    print("2. 意译")
    print("3. 口语化")

    style = input("请选择翻译风格（1/2/3）：").strip()
    text = input("请输入需要翻译的内容：").strip()

    if not text:
        print("错误：翻译内容不能为空")
        return

    try:
        result = translate(text, style)
        print("\n翻译结果：")
        print(result)
    except ValueError as error:
        print(f"输入错误：{error}")


if __name__ == "__main__":
    main()
