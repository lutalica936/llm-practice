"""统一管理第三方 OpenAI 兼容接口调用。"""

import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv(override=True)

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")
model = os.getenv("OPENAI_MODEL")

if not api_key:
    raise ValueError("未找到 OPENAI_API_KEY，请检查 .env 文件")

if not base_url:
    raise ValueError("未找到 OPENAI_BASE_URL，请检查 .env 文件")

if not model:
    raise ValueError("未找到 OPENAI_MODEL，请检查 .env 文件")


client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)


def request_document_summary(
    system_prompt: str,
    document: str,
    use_json_mode: bool = True,
) -> str:
    """调用模型并返回模型生成的原始文本。"""

    request_arguments = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": document,
            },
        ],
        "temperature": 0,
    }

    if use_json_mode:
        request_arguments["response_format"] = {
            "type": "json_object"
        }

    response = client.chat.completions.create(
        **request_arguments
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("模型返回了空内容")

    return content