# 文档结构化工具 v0.1

## 项目目标

读取一份 UTF-8 中文 TXT 文档，通过第三方 OpenAI 兼容接口，
输出核心摘要、行动项和待确认问题。

## 输入

- 第一版只支持单个 TXT 文件
- 建议长度：300—5000 个中文字符
- 仅使用合成、公开或彻底匿名的内容

## 输出结构

{
  "summary": "核心摘要",
  "actions": [
    {
      "task": "具体任务",
      "owner": null,
      "deadline": null
    }
  ],
  "questions": [
    "原文中尚未解决的问题"
  ]
}

## 字段规则

- summary 必须来自原文，不得补充外部事实
- actions 没有内容时返回空数组
- owner 和 deadline 不明确时必须为 null
- questions 没有内容时返回空数组
- 不允许根据常识猜测负责人和时间

## v0.1 包含

- 读取单个 TXT 文件
- 调用现有 llm_client
- 输出 JSON
- 基础结构校验
- 清晰的错误提示

## v0.1 不包含

- PDF、Word
- Streamlit
- RAG 或向量数据库
- 批量处理
- 多模型切换
- 数据库

## 验收标准

- 5 份匿名测试文本均能返回可解析结果
- 1000 字以上文档能够正常处理
- 输出始终包含 summary、actions、questions
- 不上传密钥和真实业务材料
