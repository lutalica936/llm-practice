# LLM Practice

一个面向初学者的 Python 与大语言模型应用练习项目。

项目使用 OpenAI Python SDK 调用第三方 OpenAI 兼容接口，目前已经完成一个“可靠文档结构化 CLI”：

- 输入一份中文 TXT 文档
- 调用大语言模型分析内容
- 输出摘要、行动项和待确认问题
- 使用 JSON 和 Pydantic 验证结果
- 支持 JSON、Markdown 两种输出格式
- 提供输入校验、超时、有限重试和中文错误提示

> 本项目仅使用合成、公开或彻底匿名的测试材料。请勿将公司内部文件、客户资料、账号信息或其他敏感数据发送给第三方 API。

## 项目目标

本项目用于练习以下能力：

- Python 虚拟环境与依赖管理
- 使用 `.env` 安全管理 API 配置
- 调用第三方 OpenAI 兼容接口
- System Prompt 与 Temperature
- JSON 结构化输出
- Pydantic 运行时数据校验
- Prompt 版本管理与 Few-shot
- LLM 测试集与自动评测
- API 超时、限流、网络错误和有限重试
- 命令行工具设计
- README、测试记录和 Git 版本管理

当前主工具可以把中文文档整理为以下结构：

```json
{
  "summary": "文档的核心摘要",
  "actions": [
    "需要执行的事项"
  ],
  "questions": [
    "需要继续确认的问题"
  ]
}
```

## 当前功能

### 文档结构化 CLI

当前 CLI 支持：

- 读取单个 UTF-8 编码的 `.txt` 文件
- 检查文件是否存在
- 拒绝目录、空文件和非 TXT 文件
- 限制输入文档最大字符数
- 选择 v1、v2 或 v3 Prompt
- 默认使用 v3 Prompt
- 优先尝试 JSON mode
- JSON mode 不兼容时自动使用 Prompt 约束方式重试
- 使用 `json.loads()` 检查 JSON 语法
- 使用 Pydantic 检查字段和数据类型
- 输出 JSON 文件
- 输出 Markdown 文件
- 保存模型原始返回内容
- 支持用户指定输出路径
- 自动创建输出目录
- 提供参数帮助和中文错误提示

### 其他练习功能

项目还包括：

- 最基础的 LLM 调用
- 中英翻译与不同翻译风格
- Temperature 对比实验
- 中文文本结构化分析
- 批量处理 TXT 文件
- 流式输出实验
- JSON mode 兼容性测试
- Prompt v1、v2、v3 对比
- 五份匿名样例自动评测
- 失败场景测试和人工复核记录

## 项目结构

```text
llm-practice/
├── evaluation/
│   ├── failure_cases.md
│   ├── manual_review.md
│   ├── prompt_scorecard.md
│   └── results.json
│
├── input/
│   └── .gitkeep
│
├── output/
│   └── .gitkeep
│
├── prompts/
│   ├── document_summarizer_v1.txt
│   ├── document_summarizer_v2.txt
│   └── document_summarizer_v3.txt
│
├── src/
│   ├── analyzer.py
│   ├── batch_process.py
│   ├── document_summarizer.py
│   ├── hello_llm.py
│   ├── llm_client.py
│   ├── schemas.py
│   ├── streaming_test.py
│   └── translator.py
│
├── tests/
│   ├── fixtures/
│   │   ├── long_report.txt
│   │   ├── meeting_actions.txt
│   │   ├── no_actions.txt
│   │   ├── questions_only.txt
│   │   └── short_note.txt
│   ├── check_models.py
│   ├── eval.py
│   ├── json_mode_test.py
│   ├── temperature_test.py
│   └── test_analyzer.py
│
├── .env.example
├── .gitignore
├── README.md
├── SPEC.md
├── compatibility.md
└── requirements.txt
```

主要文件说明：

| 文件 | 作用 |
|---|---|
| `src/document_summarizer.py` | 文档结构化 CLI 的命令行入口 |
| `src/llm_client.py` | 统一管理第三方 OpenAI 兼容接口调用 |
| `src/schemas.py` | 定义并验证文档结构化结果 |
| `prompts/` | 保存三个版本的文档结构化 Prompt |
| `tests/fixtures/` | 保存脱敏、公开或合成测试材料 |
| `tests/eval.py` | 批量运行测试样例并记录评测结果 |
| `evaluation/results.json` | 自动评测结果 |
| `evaluation/manual_review.md` | 事实性与行动项人工复核 |
| `evaluation/failure_cases.md` | 异常和失败场景测试记录 |
| `compatibility.md` | 第三方接口兼容性记录 |
| `SPEC.md` | 文档结构化工具的范围和验收标准 |

## 环境要求

建议使用：

- Python 3.9 或更高版本
- pip
- Git
- 可用的第三方 OpenAI 兼容 API

项目当前使用 Chat Completions 调用路径。第三方服务商不一定支持 OpenAI 官方接口的全部能力，实际可用的模型、参数、JSON mode、速率限制和 usage 信息以服务商文档及实测结果为准。

## 安装方法

### 1. 克隆仓库

```bash
git clone <你的仓库地址>
cd llm-practice
```

如果项目已经在本地，只需要进入项目目录：

```bash
cd /Users/hstsmacbook/Projects/llm-practice
```

### 2. 创建虚拟环境

macOS 或 Linux：

```bash
python3 -m venv .venv
```

Windows：

```powershell
python -m venv .venv
```

### 3. 激活虚拟环境

macOS 或 Linux：

```bash
source .venv/bin/activate
```

Windows PowerShell：

```powershell
.venv\Scripts\Activate.ps1
```

激活成功后，终端提示符前通常会出现：

```text
(.venv)
```

### 4. 安装依赖

```bash
python -m pip install -r requirements.txt
```

## 配置第三方 API

### 1. 复制环境变量示例

macOS 或 Linux：

```bash
cp .env.example .env
```

Windows PowerShell：

```powershell
Copy-Item .env.example .env
```

### 2. 编辑 `.env`

填写第三方服务商提供的信息：

```dotenv
OPENAI_API_KEY=你的真实API密钥
OPENAI_BASE_URL=https://你的服务商地址/v1
OPENAI_MODEL=你的模型名称
```

三个配置项分别表示：

| 配置项 | 作用 |
|---|---|
| `OPENAI_API_KEY` | 调用接口所需的密钥 |
| `OPENAI_BASE_URL` | 第三方 OpenAI 兼容接口地址 |
| `OPENAI_MODEL` | 服务商提供的模型名称 |

不要把真实密钥写进 Python 文件，也不要把 `.env` 上传到 GitHub。

配置完成后，可以检查 Git 是否忽略 `.env`：

```bash
git status --short --ignored
```

正常情况下，`.env` 不应出现在准备提交的文件中。

## 使用文档结构化工具

所有命令都应在项目根目录执行。

运行前先确认虚拟环境已经激活：

```bash
source .venv/bin/activate
```

### 查看参数帮助

```bash
python src/document_summarizer.py --help
```

CLI 支持以下主要参数：

| 参数 | 是否必填 | 说明 |
|---|---:|---|
| `input_file` | 是 | UTF-8 编码的 TXT 输入文件 |
| `--prompt-version` | 否 | `v1`、`v2` 或 `v3`，默认 `v3` |
| `--format` | 否 | `json` 或 `markdown`，默认 `json` |
| `--output` | 否 | 自定义最终结果保存路径 |

### 最简单的运行方式

```bash
python src/document_summarizer.py \
  tests/fixtures/short_note.txt
```

这条命令会：

1. 读取 `short_note.txt`
2. 使用默认的 v3 Prompt
3. 调用第三方 API
4. 验证模型返回的 JSON
5. 在终端显示处理结果
6. 把文件保存到 `output/`

默认会生成类似以下文件：

```text
output/short_note_v3_raw.txt
output/short_note_v3.json
```

其中：

- `raw.txt` 保存模型未经二次排版的原始返回
- `.json` 保存经过 JSON 和 Pydantic 校验的最终结果

### 选择 Prompt 版本

使用 v1：

```bash
python src/document_summarizer.py \
  tests/fixtures/short_note.txt \
  --prompt-version v1
```

使用 v2：

```bash
python src/document_summarizer.py \
  tests/fixtures/short_note.txt \
  --prompt-version v2
```

使用 v3：

```bash
python src/document_summarizer.py \
  tests/fixtures/short_note.txt \
  --prompt-version v3
```

如果没有填写 `--prompt-version`，程序默认使用 v3。

三个版本的主要定位：

| 版本 | 主要用途 |
|---|---|
| v1 | 最基础的结构化要求 |
| v2 | 增加更明确的字段、事实性和格式约束 |
| v3 | 在明确约束基础上增加 Few-shot 示例 |

### 输出 JSON

```bash
python src/document_summarizer.py \
  tests/fixtures/meeting_actions.txt \
  --prompt-version v3 \
  --format json \
  --output output/meeting_actions.json
```

输出示例：

```json
{
  "summary": "项目组讨论了上线前测试和材料确认工作。",
  "actions": [
    "完成上线前功能测试",
    "整理最终版本的说明材料"
  ],
  "questions": [
    "最终上线日期是否已经确认？"
  ]
}
```

JSON 更适合：

- 其他 Python 程序继续读取
- 自动评测
- 数据统计
- 后续接入界面或其他系统

可以使用 Python 检查 JSON 是否有效：

```bash
python -m json.tool output/meeting_actions.json
```

如果文件是合法 JSON，终端会显示格式化后的内容。

### 输出 Markdown

```bash
python src/document_summarizer.py \
  tests/fixtures/long_report.txt \
  --prompt-version v3 \
  --format markdown \
  --output output/long_report.md
```

输出示例：

```markdown
# 文档结构化结果

## 摘要

项目组讨论了上线前的主要准备工作。

## 行动项

1. 完成功能测试
2. 整理上线材料

## 待确认问题

1. 最终上线时间是否确定？
```

Markdown 更适合：

- 人工阅读
- 复制到笔记软件
- 放入项目文档
- 生成可展示的示例结果

### 使用默认输出路径

如果不填写 `--output`：

```bash
python src/document_summarizer.py \
  tests/fixtures/long_report.txt \
  --format markdown
```

程序会自动把最终结果保存在 `output/` 目录。

### 使用自定义输出目录

```bash
python src/document_summarizer.py \
  tests/fixtures/long_report.txt \
  --format markdown \
  --output output/examples/long_report.md
```

如果 `output/examples/` 不存在，程序会自动创建。

### 输出格式与扩展名必须一致

JSON 输出必须使用 `.json`：

```bash
python src/document_summarizer.py \
  tests/fixtures/short_note.txt \
  --format json \
  --output output/result.json
```

Markdown 输出必须使用 `.md`：

```bash
python src/document_summarizer.py \
  tests/fixtures/short_note.txt \
  --format markdown \
  --output output/result.md
```

下面的命令会被拒绝：

```bash
python src/document_summarizer.py \
  tests/fixtures/short_note.txt \
  --format markdown \
  --output output/result.json
```

因为 `markdown` 格式与 `.json` 扩展名不一致。

## 输入要求

当前版本的输入文件必须满足以下要求：

- 必须是一个真实存在的文件
- 文件扩展名必须是 `.txt`
- 文件编码必须是 UTF-8
- 文件内容不能为空
- 文件内容不能超过程序设置的最大字符数
- 内容只能使用合成、公开或彻底匿名的材料

检查测试文件字符数：

```bash
python -c "from pathlib import Path; p=Path('tests/fixtures/long_report.txt'); print(len(p.read_text(encoding='utf-8')))"
```

当前版本暂不支持：

- PDF
- Word
- 图片
- Excel
- 网页地址
- 一次处理多个文件
- RAG 或向量数据库
- 自动拆分超长文档

## 数据处理流程

```text
TXT 测试文档
    ↓
document_summarizer.py 读取并校验输入
    ↓
读取 prompts/ 中指定版本的 Prompt
    ↓
llm_client.py 调用第三方 OpenAI 兼容接口
    ↓
模型返回 JSON 文本
    ↓
json.loads() 检查 JSON 语法
    ↓
Pydantic 检查字段和数据类型
    ↓
保存原始返回
    ↓
生成 JSON 或 Markdown 最终结果
```

其中：

- `json.loads()` 检查引号、逗号和括号等 JSON 语法
- Pydantic 检查 `summary`、`actions` 和 `questions` 是否存在及类型是否正确
- JSON 和 Markdown 输出都来自同一份通过验证的数据
- 切换 Markdown 输出不会再次调用模型

## 错误处理

程序会处理以下常见问题：

### 文件不存在

```bash
python src/document_summarizer.py missing.txt
```

程序会提示文件不存在，而不是直接显示难懂的错误堆栈。

### 输入文件为空

如果 TXT 文件没有有效内容，程序会在调用 API 前停止。

这样可以避免：

- 浪费 API 调用
- 产生无意义结果
- 增加不必要的费用

### 输入格式错误

当前版本只支持 TXT：

```bash
python src/document_summarizer.py README.md
```

程序会提示：

```text
当前版本只支持 TXT 文件
```

### 输入过长

如果文档超过当前限制，程序会显示：

- 当前字符数
- 最大允许字符数
- 缩短或拆分文档的建议

### API 配置缺失

如果 `.env` 中缺少配置，程序会提示检查：

- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`
- `OPENAI_MODEL`

### JSON mode 不兼容

程序会优先尝试：

```python
response_format={"type": "json_object"}
```

如果第三方服务商明确提示不支持 JSON mode，程序会去掉 `response_format`，改用 Prompt 约束方式重试。

### 模型返回的不是合法 JSON

如果模型返回内容存在 JSON 语法错误，程序会提示具体的解析行号和列号。

### JSON 结构不符合要求

即使 JSON 语法正确，如果缺少字段或字段类型错误，Pydantic 也会拒绝结果。

例如，下面的内容不是有效结果：

```json
{
  "summary": "文档摘要"
}
```

因为它缺少：

- `actions`
- `questions`

### 超时、网络错误和限流

程序对以下暂时性错误进行有限重试：

- 请求超时
- 网络连接失败
- HTTP 429 限流
- 部分 HTTP 5xx 服务端错误

重试次数有明确上限，不会无限调用接口。

日志只显示必要的错误类型和重试进度，不打印：

- API Key
- 完整输入正文
- 完整请求参数

## 检查程序退出码

成功运行后：

```bash
python src/document_summarizer.py --help
echo $?
```

预期退出码：

```text
0
```

测试不存在的文件：

```bash
python src/document_summarizer.py missing.txt
echo $?
```

预期结果为非零退出码。

一般约定：

| 退出码 | 含义 |
|---:|---|
| `0` | 成功 |
| `1` | API、网络、认证或其他运行错误 |
| `2` | 输入参数、文件、JSON 或数据校验错误 |

## 自动评测

运行评测前，请确认：

- 虚拟环境已激活
- `.env` 配置正确
- 测试材料不包含敏感信息
- 第三方 API 当前可用

执行：

```bash
python tests/eval.py
```

评测会使用固定测试集，对多个 Prompt 版本进行比较。

建议至少记录：

- 是否成功解析
- 处理耗时
- usage 信息（如果服务商返回）
- 摘要事实性
- 行动项准确性
- 问题覆盖度
- 失败原因

如果第三方接口不返回 usage，应明确记录为：

```text
N/A
```

不要把缺失数据误写成 0。

## 其他练习脚本

### 基础调用

```bash
python src/hello_llm.py
```

用于理解一次最基础的模型请求。

### 中英翻译

```bash
python src/translator.py
```

用于比较直译、意译和口语化三种 System Prompt。

### 结构化文本分析

```bash
python src/analyzer.py
```

用于练习：

- JSON 输出
- `json.loads()`
- 基础业务校验
- 中文文本分析

### 批量处理

```bash
python src/batch_process.py
```

脚本会遍历 `input/` 中的 TXT 文件，并把结果写入 `output/`。

### 流式输出

```bash
python src/streaming_test.py
```

用于观察模型内容逐步返回的过程。

## 安全与隐私

使用本项目时必须遵守以下规则：

### 禁止发送的内容

不要向第三方 API 发送：

- 公司内部文件
- 客户资料
- 未公开业务数据
- 账号和密码
- API Key
- 身份证号、手机号等个人信息
- 受保密协议约束的内容
- 无法确认是否可以外发的材料

### 允许使用的内容

优先使用：

- 自己编写的合成文档
- 已公开的材料
- 已获得明确授权的材料
- 经过彻底匿名处理的测试文本

### Git 提交前检查

```bash
git status --short
git diff --check
git diff
```

确认以下内容没有进入提交：

- `.env`
- API Key
- `.venv/`
- 模型生成的临时输出
- 真实公司或客户材料
- 包含敏感数据的日志

不要为了省事直接执行：

```bash
git add .
```

更安全的方式是明确添加需要提交的文件：

```bash
git add src/document_summarizer.py README.md
```

## 常见问题

### 1. 为什么已经使用 JSON mode，还需要 Pydantic？

JSON mode 主要保证返回内容是合法 JSON，但不一定保证：

- 所有字段都存在
- 字段类型正确
- 没有额外字段
- 字符串不是空值

因此仍需使用 Pydantic 做业务结构验证。

### 2. 为什么还要保存模型原始返回？

保存原始返回有助于定位：

- JSON 解析失败
- Prompt 约束不足
- 第三方接口兼容性问题
- 不同 Prompt 版本之间的差异

原始返回只用于本地测试，不应包含真实敏感内容。

### 3. 为什么默认使用 v3 Prompt？

v3 在明确字段和事实性约束的基础上加入了 Few-shot 示例，更容易让模型理解预期结构。

最终应以评测结果选择 Prompt，而不是只凭主观感觉判断。

### 4. 为什么不直接支持 PDF、Word、RAG 和界面？

当前阶段的重点是先完成最小、可靠、可验证的闭环：

```text
TXT 输入
→ 模型处理
→ 结构校验
→ 文件输出
```

只有测试或用户反馈证明有必要时，才继续增加 PDF、Word、界面、RAG 或其他复杂功能。

### 5. 为什么输出目录里的文件没有出现在 Git 状态中？

`output/` 通常会被 `.gitignore` 忽略，因为模型输出可能：

- 数量较多
- 每次运行都会变化
- 意外包含不适合公开的信息

如需展示示例，建议单独建立经过检查的脱敏示例目录。

## 当前已知限制

- 只支持 UTF-8 TXT 文件
- 一次只处理一个文件
- 最大长度按字符数而不是 token 数计算
- 第三方接口可能不支持完整的 OpenAI 官方能力
- 部分服务商可能不返回 usage
- 当前 `actions` 是字符串列表
- 尚未支持负责人和截止时间等行动项子字段
- 尚未支持自动拆分超长文档
- 尚未提供图形界面
- 模型结果仍需进行事实性人工复核

## 开发进度

### W2：OpenAI 兼容 API 工程化

- [x] 跑通第一次第三方 API 调用
- [x] 使用 `.env` 管理配置
- [x] 理解消息角色和 Temperature
- [x] 实现 JSON 结构化输出
- [x] 增加异常处理
- [x] 完成批量处理
- [x] 完成流式输出练习

### W3：可靠文档结构化 CLI

- [x] 明确项目范围和验收标准
- [x] 创建 CLI 项目骨架
- [x] 准备匿名测试材料
- [x] 接入共用 `llm_client.py`
- [x] 使用 Pydantic 验证模型输出
- [x] 实现 Prompt v1、v2、v3
- [x] 增加 Few-shot 示例
- [x] 建立自动评测流程
- [x] 增加输入校验
- [x] 增加超时、有限重试和错误分类
- [x] 增加日志脱敏
- [x] 支持 JSON 和 Markdown 输出
- [x] 完善参数帮助和 README
- [ ] 完成最终回归测试
- [ ] 整理 Prompt 迭代日志
- [ ] 发布 v0.1.0

## v0.1 验收标准

发布 v0.1.0 前应满足：

- 5 份匿名样例都能返回可解析结果
- 1000 字以上中文输入可以正常处理
- 输出始终包含 `summary`、`actions` 和 `questions`
- JSON 文件可以被 `python -m json.tool` 解析
- Markdown 文件包含摘要、行动项和待确认问题
- 常见输入错误有清晰中文提示
- 成功和失败使用合理的退出码
- README 中的主要命令经过实际验证
- 仓库不包含密钥和真实敏感数据
- 能解释最佳 Prompt、已知限制和第三方接口兼容点

## 提交建议

完成 CLI 和 README 后：

```bash
git status --short
git diff --check
git diff -- src/document_summarizer.py README.md
```

确认无误后提交：

```bash
git add src/document_summarizer.py README.md
git commit -m "feat: improve cli output and documentation"
```

## 项目定位

这是一个个人学习项目，重点不是堆叠热门框架，而是建立一个完整、清晰、可验证的 LLM 应用开发过程：

```text
明确范围
→ 准备测试材料
→ 实现最小功能
→ 结构化输出
→ 运行时校验
→ 自动评测
→ 异常处理
→ 文档和复盘
```

当前实现以学习清晰度、接口兼容性、安全性和可复现性为优先目标，不代表生产环境方案。