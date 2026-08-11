import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


# 将项目根目录加入 Python 的查找路径，并读取根目录下的 .env
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")
model = os.getenv("OPENAI_MODEL")

if not api_key:
    sys.exit("错误：.env 中缺少 OPENAI_API_KEY")

if not base_url:
    sys.exit("错误：.env 中缺少 OPENAI_BASE_URL")

if not model:
    sys.exit("错误：.env 中缺少 OPENAI_MODEL")

client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)

print("正在测试 JSON mode……")
print(f"当前模型：{model}")

try:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "你只能输出合法的 JSON 对象，不要输出解释或 Markdown。",
            },
            {
                "role": "user",
                "content": '请返回一个包含 status 和 message 字段的 JSON 对象，status 的值为 ok。',
            },
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )

    raw_text = response.choices[0].message.content

    if not raw_text:
        sys.exit("测试失败：模型返回了空内容")

    print("\n模型原始返回：")
    print(raw_text)

    parsed_data = json.loads(raw_text)

    print("\nJSON 解析成功：")
    print(json.dumps(parsed_data, ensure_ascii=False, indent=2))

    if parsed_data.get("status") == "ok":
        print("\n测试通过：当前接口支持本次 JSON mode 调用。")
    else:
        print("\nJSON 可以解析，但 status 不是预期的 ok。")

except json.JSONDecodeError as exc:
    print("\n测试失败：模型返回的内容不是合法 JSON。")
    print(f"解析位置：第 {exc.lineno} 行，第 {exc.colno} 列")

except Exception as exc:
    print("\n接口调用失败。")
    print(f"错误类型：{type(exc).__name__}")
    print(f"错误信息：{exc}")