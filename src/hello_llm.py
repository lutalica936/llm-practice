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

response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "user",
            "content": "你好，请用三句话介绍你自己。",
        }
    ],
)

print(response.choices[0].message.content)