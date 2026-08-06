import json
import os
from typing import Any, Dict, List, TypedDict

from dotenv import load_dotenv

from openai import (
    OpenAI,
    AuthenticationError,
    RateLimitError,
    APIConnectionError,
    InternalServerError,
    BadRequestError,
)


# =========================
# 1. 加载环境变量
# =========================

load_dotenv(override=True)


api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")
model = os.getenv("OPENAI_MODEL")


if not api_key:
    raise ValueError(
        "没有读取到 OPENAI_API_KEY，请检查 .env 文件"
    )

if not base_url:
    raise ValueError(
        "没有读取到 OPENAI_BASE_URL，请检查 .env 文件"
    )

if not model:
    raise ValueError(
        "没有读取到 OPENAI_MODEL，请检查 .env 文件"
    )


# =========================
# 2. 创建 OpenAI Client
# =========================

client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)


# =========================
# 3. 定义返回数据结构
# =========================

class AnalysisResult(TypedDict):
    sentiment: str
    keywords: List[str]
    summary: str



# =========================
# 4. System Prompt
# =========================

SYSTEM_PROMPT = """
你是一名中文文本分析助手。

请分析用户提供的中文文本，并返回一个合法的 JSON 对象。

JSON 必须严格包含以下三个字段：

1. sentiment：
   字符串，只能是：
   "正面"
   "中性"
   "负面"

2. keywords：
   字符串数组，提取3～5个关键词

3. summary：
   字符串，用一句简洁中文总结文本


必须遵守：

- 只返回 JSON
- 不返回分析过程
- 不返回 Markdown
- 不添加额外说明
- 所有字段必须存在


示例：

{
  "sentiment": "正面",
  "keywords": [
    "项目",
    "客户",
    "合作"
  ],
  "summary": "项目顺利完成并获得客户认可。"
}

""".strip()



# =========================
# 5. JSON业务校验
# =========================

def validate_result(
    data: Dict[str, Any]
) -> AnalysisResult:
    """
    检查模型返回的数据是否符合业务要求
    """

    required_keys = {
        "sentiment",
        "keywords",
        "summary"
    }


    if set(data.keys()) != required_keys:
        raise ValueError(
            f"字段错误，需要字段：{required_keys}，"
            f"实际字段：{set(data.keys())}"
        )


    if data["sentiment"] not in {
        "正面",
        "中性",
        "负面"
    }:
        raise ValueError(
            f"sentiment值错误：{data['sentiment']}"
        )


    if not isinstance(
        data["keywords"],
        list
    ):
        raise ValueError(
            "keywords必须是列表"
        )


    if not 3 <= len(data["keywords"]) <= 5:
        raise ValueError(
            "keywords数量必须为3～5个"
        )


    if not all(
        isinstance(k, str)
        for k in data["keywords"]
    ):
        raise ValueError(
            "keywords必须全部是字符串"
        )


    if not isinstance(
        data["summary"],
        str
    ):
        raise ValueError(
            "summary必须是字符串"
        )


    if not data["summary"].strip():
        raise ValueError(
            "summary不能为空"
        )


    return {
        "sentiment": data["sentiment"],
        "keywords": data["keywords"],
        "summary": data["summary"],
    }



# =========================
# 6. 调用LLM
# =========================

def analyze_text(
    text: str
) -> AnalysisResult:


    if not text.strip():
        raise ValueError(
            "输入文本不能为空"
        )


    try:

        response = client.chat.completions.create(

            model=model,

            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content":
                    f"请分析以下文本：\n\n{text}"
                }
            ],


            temperature=0,

            max_tokens=500,


            # 如果第三方不支持，
            # 会触发 BadRequestError
            response_format={
                "type": "json_object"
            }
        )


    except AuthenticationError:

        raise ValueError(
            "API Key错误，请检查OPENAI_API_KEY"
        )


    except RateLimitError:

        raise ValueError(
            "请求次数过多或API额度不足，请稍后重试"
        )


    except APIConnectionError:

        raise ValueError(
            "网络连接失败，请检查网络或代理"
        )


    except InternalServerError:

        raise ValueError(
            "服务器异常（500/503），请稍后重试"
        )


    except BadRequestError as error:

        raise ValueError(
            f"请求参数错误，可能是不支持response_format：{error}"
        )


    except Exception as error:

        raise ValueError(
            f"未知API错误：{error}"
        )



    # =========================
    # 7. 解析JSON
    # =========================


    raw_content = (
        response
        .choices[0]
        .message
        .content
    )


    if raw_content is None:

        raise ValueError(
            "模型没有返回内容"
        )


    try:

        parsed_data = json.loads(
            raw_content
        )


    except json.JSONDecodeError as error:

        print("\n模型原始输出:")
        print(raw_content)

        raise ValueError(
            f"模型返回不是合法JSON：{error}"
        )


    if not isinstance(
        parsed_data,
        dict
    ):

        raise ValueError(
            "JSON顶层必须是对象"
        )


    return validate_result(
        parsed_data
    )



# =========================
# 8. 主程序
# =========================

def main():

    print(
        "====== 中文文本分析工具 ======"
    )


    text = input(
        "请输入需要分析的文本：\n"
    ).strip()


    try:

        result = analyze_text(
            text
        )


    except ValueError as error:

        print(
            "\n分析失败："
        )

        print(error)

        return



    print(
        "\n分析成功："
    )


    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2
        )
    )


    print(
        "\n字段读取测试："
    )


    print(
        f"情感：{result['sentiment']}"
    )

    print(
        f"关键词：{'、'.join(result['keywords'])}"
    )

    print(
        f"摘要：{result['summary']}"
    )



if __name__ == "__main__":

    main()