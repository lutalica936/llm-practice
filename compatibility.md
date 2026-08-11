# 第三方 OpenAI 兼容接口测试记录

## 测试环境

- 测试日期：2026-08-11
- SDK：OpenAI Python SDK
- 调用路径：Chat Completions
- 模型：填写实际模型名称
- 测试数据：合成文本

## JSON mode

- 是否接受 response_format：是 / 否
- 是否能返回合法 JSON：是 / 否
- json.loads 是否成功：是 / 否
- Pydantic 是否成功：是 / 否

## 三个测试样例

| 文件 | JSON 解析 | Pydantic 校验 | 人工事实检查 |
|---|---|---|---|
| short_note.txt | 通过/失败 | 通过/失败 | 通过/失败 |
| meeting_actions.txt | 通过/失败 | 通过/失败 | 通过/失败 |
| long_report.txt | 通过/失败 | 通过/失败 | 通过/失败 |

## 兼容性结论

主方案：填写实际测试结论。

兜底方案：服务商不支持 JSON mode 时，删除
response_format 参数，依靠 Prompt 约束返回 JSON，
随后继续执行 json.loads 和 Pydantic 校验。
