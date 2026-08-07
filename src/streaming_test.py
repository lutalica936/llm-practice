import os

from dotenv import load_dotenv
from openai import OpenAI

from llm_client import client


load_dotenv()


# client = OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY"),
#     base_url=os.getenv("OPENAI_BASE_URL"),
# )


response = client.chat.completions.create(
    model="gpt-5.5",
    messages=[
        {
            "role": "user",
            "content": "介绍一下人工智能的发展历史",
        }
    ],
    stream=True,
)


for chunk in response:
    # 某些第三方中转会返回 choices=[] 的结束事件
    if not chunk.choices:
        continue

    content = chunk.choices[0].delta.content

    if content:
        print(content, end="", flush=True)


print()