# 第三方 OpenAI 兼容接口记录

## W2 已验证

- OpenAI Python SDK 可以通过自定义 base_url 调用
- API Key 通过 .env 管理
- 普通文本生成可用
- 当前调用路径：填写 src/llm_client.py 中实际使用的路径
- 当前模型环境变量：填写实际变量名称

## W3 待验证

- 是否支持 JSON mode
- 是否支持 response_format
- 是否返回 usage
- 超时和限流时返回什么异常
- 最大可接受输入长度

## 执行原则

W3 沿用已经跑通的调用路径，不同时维护 Responses 和
Chat Completions 两套实现。
