"""定义文档结构化工具的标准输出格式。"""

from pydantic import BaseModel, ConfigDict, Field


class DocumentResult(BaseModel):
    """经过验证的文档结构化结果。"""

    model_config = ConfigDict(extra="forbid")

    summary: str = Field(
        min_length=1,
        description="对原文主要内容的简洁摘要",
    )

    actions: list[str] = Field(
        description="从原文提取的明确行动项",
    )

    questions: list[str] = Field(
        description="原文中需要继续确认的问题",
    )