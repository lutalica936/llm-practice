import os

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


def generate_text(temperature: float) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "你是一名擅长创意写作的中文文案助手。",
            },
            {
                "role": "user",
                "content": "为一家位于海边的咖啡店写一句不超过30字的宣传语。",
            },
        ],
        temperature=temperature,
        max_tokens=100,
    )

    return response.choices[0].message.content


for temperature in [0, 1]:
    print(f"\n===== temperature={temperature} =====")

    for number in range(1, 6):
        result = generate_text(temperature)
        print(f"{number}. {result}")

