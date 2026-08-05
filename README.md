# LLM Practice

这是一个用于学习 Python 工程化和 LLM API 调用的练习项目。

## 项目目标

通过这个项目学习：

- 使用 Python 调用 OpenAI 兼容接口
- 使用 `.env` 管理 API Key
- 使用 Git 和 GitHub 管理代码
- 处理结构化输出和常见 API 异常
- 批量处理文本文件

## 项目结构

```text
llm-practice/
├── input/                 # 待处理的输入文件
├── output/                # 模型生成的结果
├── src/                   # Python 源代码
│   └── hello_llm.py       # 最基础的 LLM 调用示例
├── .env.example           # 环境变量示例
├── .gitignore             # Git 忽略规则
├── README.md              # 项目说明
└── requirements.txt       # Python 依赖列表
```

## 环境要求

- Python 3.9 或更高版本
- pip
- 可用的 OpenAI 兼容 API

## 安装方法

### 1. 创建虚拟环境

```bash
python3 -m venv .venv
```

### 2. 激活虚拟环境

macOS 或 Linux：

```bash
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

## 配置环境变量

复制环境变量示例文件：

```bash
cp .env.example .env
```

然后打开 `.env`，填写自己的配置：

```dotenv
VIPTOKEN_API_KEY=your_api_key_here
VIPTOKEN_BASE_URL=https://your-api-provider.example
OPENAI_MODEL=your_model_name
```

`.env` 中包含真实 API Key，不要把它提交到 GitHub。

## 运行程序

确保已经激活虚拟环境，然后执行：

```bash
python src/hello_llm.py
```

## 当前脚本

### hello_llm.py

向 LLM 发送一段文本，并在终端打印模型回复。

## 学习进度

- [x] Day 1：完成第一次 LLM API 调用
- [x] Day 2：完成项目结构和环境变量配置
- [ ] Day 3：System Prompt 与参数实验
- [ ] Day 4：结构化 JSON 输出
- [ ] Day 5：异常处理与自动重试
- [ ] Day 6：批量处理与流式输出
- [ ] Day 7：项目整理与复盘

## 安全说明

- 不要在代码中硬编码 API Key
- 不要把 `.env` 上传到 GitHub
- 如果密钥意外泄露，应立即删除旧密钥并创建新密钥