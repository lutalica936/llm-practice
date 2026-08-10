# LLM Practice

一个用于练习 Python 工程化、第三方 OpenAI 兼容 API 调用和 LLM 应用开发的项目。

项目从基础调用开始，逐步覆盖环境变量管理、Prompt 设计、结构化输出、异常处理、批量处理和流式输出。目前正在开发一个“文档结构化工具”，目标是将中文长文档整理为摘要、行动项和待确认问题。

## 当前能力

- 使用 OpenAI Python SDK 调用第三方兼容接口
- 通过 `.env` 管理 API Key、Base URL 和模型名称
- 使用不同 System Prompt 控制翻译风格
- 获取并校验结构化 JSON 输出
- 批量处理 `input/` 中的文本文件
- 流式打印模型输出
- 读取并检查文档摘要器的 TXT 输入文件

## 项目结构

```text
llm-practice/
├── input/                         # 批量处理脚本的输入文件
├── output/                        # 模型生成结果（不提交到 Git）
├── prompts/
│   └── document_summarizer_v1.txt # 文档摘要器 Prompt（W3 开发中）
├── src/
│   ├── analyzer.py                # 中文文本结构化分析
│   ├── batch_process.py           # 批量处理 input/ 中的文本
│   ├── document_summarizer.py     # 文档结构化工具（当前为 CLI 骨架）
│   ├── hello_llm.py               # 最基础的 LLM 调用示例
│   ├── llm_client.py              # 共用 OpenAI 客户端
│   ├── streaming_test.py          # 流式输出示例
│   └── translator.py              # 三种风格的中英翻译工具
├── tests/
│   ├── fixtures/                  # 文档摘要器的固定测试材料
│   │   ├── long_report.txt
│   │   ├── meeting_actions.txt
│   │   └── short_note.txt
│   ├── temperature_test.py        # Temperature 对比实验
│   └── test_analyzer.py           # 结构化分析测试
├── .env.example                   # 环境变量示例
├── .gitignore                     # Git 忽略规则
├── README.md                      # 项目说明
├── requirements.txt               # Python 依赖
└── SPEC.md                        # 文档结构化工具 v0.1 规格
```

## 环境要求

- Python 3.9 或更高版本
- pip
- 可用的第三方 OpenAI 兼容 API

## 安装

### 1. 克隆并进入项目

```bash
git clone <your-repository-url>
cd llm-practice
```

### 2. 创建并激活虚拟环境

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell：

```powershell
.venv\Scripts\Activate.ps1
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

## 配置

复制环境变量示例：

```bash
cp .env.example .env
```

编辑 `.env`：

```dotenv
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://your-api-provider.example/v1
OPENAI_MODEL=your_model_name
```

第三方接口可能只兼容部分 OpenAI API 能力，实际支持的模型、参数、JSON 模式和速率限制以服务商说明及实测结果为准。

## 使用方法

运行前请确认已激活虚拟环境，并从项目根目录执行命令。

### 基础调用

```bash
python src/hello_llm.py
```

向模型发送一条简单消息并打印回复。

### 中英翻译

```bash
python src/translator.py
```

按提示选择直译、意译或口语化风格，再输入需要翻译的文本。

### 结构化文本分析

```bash
python src/analyzer.py
```

将中文文本整理为包含情感、关键词和摘要的 JSON 对象，并进行基础业务校验。

### 批量处理

将 `.txt` 文件放入 `input/`，然后执行：

```bash
python src/batch_process.py
```

结果会写入 `output/`，终端会显示成功和失败数量。

### 流式输出

```bash
python src/streaming_test.py
```

观察模型生成内容时逐步返回文本的效果。

### 文档结构化工具

当前版本已经完成 TXT 文件读取、格式检查和命令行入口，尚未接入 LLM 摘要与 JSON 校验。

```bash
python src/document_summarizer.py tests/fixtures/short_note.txt
```

查看参数帮助：

```bash
python src/document_summarizer.py --help
```

计划中的 v0.1 输出结构：

```json
{
  "summary": "文档核心摘要",
  "actions": [
    {
      "task": "需要执行的事项",
      "owner": null,
      "deadline": null
    }
  ],
  "questions": [
    "原文中尚未解决的问题"
  ]
}
```

详细范围和验收标准见 [`SPEC.md`](SPEC.md)。

## 学习进度

### W2：LLM API 基础

- [x] 第一次调用第三方 OpenAI 兼容 API
- [x] 使用 `.env` 管理配置和密钥
- [x] 测试消息角色和 Temperature
- [x] 获取并校验结构化 JSON
- [x] 增加常见 API 异常处理
- [x] 完成批量处理和流式输出练习

### W3：可靠文档结构化工具

- [x] 明确 v0.1 范围和输出结构
- [x] 创建 CLI 骨架和输入文件检查
- [x] 准备短文档、长文档和会议记录测试材料
- [ ] 接入现有 `llm_client.py`
- [ ] 使用 Pydantic 校验模型输出
- [ ] 比较多个 Prompt 版本
- [ ] 建立小型自动评测流程
- [ ] 补充异常处理、README 示例和最终复盘

## 安全说明

- 不在代码中硬编码 API Key
- 不提交 `.env`、`.venv` 和模型输出目录
- 不将公司内部、客户、账号或个人敏感信息发送到第三方 API
- 测试和公开展示只使用合成、公开或彻底匿名的数据
- 如果密钥意外泄露，应立即停用旧密钥并创建新密钥

## 当前定位

这是一个个人学习项目，重点是记录从基础 API 调用到可验证 LLM 工具的完整过程。当前代码以学习清晰度和可复现性为主，不代表生产环境实现。
