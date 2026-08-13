"""统一管理第三方 OpenAI 兼容接口调用。"""

import os
import time

from dotenv import load_dotenv
from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    OpenAI,
    RateLimitError,
)


# 从项目根目录的 .env 文件读取配置。
load_dotenv(override=True)

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")
model = os.getenv("OPENAI_MODEL")


# 单次请求最多等待 300 秒。
REQUEST_TIMEOUT_SECONDS = 300.0

# 失败后的最大重试次数。
# 不包括第一次正常调用。
# 因此，MAX_RETRIES = 2 表示最多调用 3 次：
# 第一次调用 + 两次重试。
MAX_RETRIES = 2

# 第一次重试前等待 2 秒。
# 第二次重试前等待 4 秒。
INITIAL_RETRY_WAIT_SECONDS = 2.0


if not api_key:
    raise ValueError(
        "未找到 OPENAI_API_KEY，请检查 .env 文件"
    )

if not base_url:
    raise ValueError(
        "未找到 OPENAI_BASE_URL，请检查 .env 文件"
    )

if not model:
    raise ValueError(
        "未找到 OPENAI_MODEL，请检查 .env 文件"
    )


client = OpenAI(
    api_key=api_key,
    base_url=base_url,
    timeout=REQUEST_TIMEOUT_SECONDS,

    # OpenAI SDK 默认可能自动重试。
    # 这里关闭 SDK 自带重试，
    # 统一使用本文件中清晰、可控的重试逻辑。
    max_retries=0,
)


def is_retryable_status_code(
    status_code: int,
) -> bool:
    """判断 HTTP 状态码是否适合有限重试。"""

    if status_code in {
        408,
        409,
        429,
    }:
        return True

    if status_code >= 500:
        return True

    return False


def is_retryable_error(
    error: Exception,
) -> bool:
    """判断异常是否属于暂时性错误。"""

    if isinstance(
        error,
        (
            APITimeoutError,
            APIConnectionError,
            RateLimitError,
        ),
    ):
        return True

    if isinstance(error, APIStatusError):
        return is_retryable_status_code(
            error.status_code
        )

    return False


def request_with_retry(
    request_arguments: dict,
):
    """
    调用 Chat Completions 接口，并处理暂时性错误。

    第一次失败后等待 2 秒；
    第二次失败后等待 4 秒；
    第三次仍然失败时结束，不再继续调用。
    """

    for attempt in range(
        MAX_RETRIES + 1
    ):
        try:
            return client.chat.completions.create(
                **request_arguments
            )

        except Exception as error:
            # 认证失败、参数错误等不可恢复错误
            # 不应重复发送请求。
            if not is_retryable_error(error):
                raise

            # attempt 从 0 开始：
            # attempt == 0：第一次调用失败；
            # attempt == 1：第一次重试失败；
            # attempt == 2：第二次重试失败。
            if attempt >= MAX_RETRIES:
                raise RuntimeError(
                    "接口暂时不可用，"
                    f"已完成 {MAX_RETRIES} 次重试，"
                    "请稍后重新运行"
                ) from error

            retry_number = attempt + 1

            # 采用简单的指数退避：
            # 第一次等待 2 秒，第二次等待 4 秒。
            wait_seconds = (
                INITIAL_RETRY_WAIT_SECONDS
                * (2 ** attempt)
            )

            # 这里只显示错误类型和重试进度。
            # 不打印 API Key、完整正文或完整请求参数。
            print(
                "\n提示：接口请求暂时失败。"
            )
            print(
                f"错误类型：{type(error).__name__}"
            )
            print(
                f"{wait_seconds:.0f} 秒后进行"
                f"第 {retry_number}/{MAX_RETRIES} 次重试……"
            )

            time.sleep(
                wait_seconds
            )

    # 正常情况下不会执行到这里。
    raise RuntimeError(
        "接口调用未返回结果"
    )


def request_document_summary(
    system_prompt: str,
    document: str,
    use_json_mode: bool = True,
) -> str:
    """调用模型并返回模型生成的原始文本。"""

    if not system_prompt.strip():
        raise ValueError(
            "System Prompt 不能为空"
        )

    if not document.strip():
        raise ValueError(
            "输入文档不能为空"
        )

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

    response = request_with_retry(
        request_arguments
    )

    content = (
        response
        .choices[0]
        .message
        .content
    )

    if not content:
        raise ValueError(
            "模型返回了空内容"
        )

    return content