from analyzer import analyze_text


TEST_TEXT = """
公司新上线的办公系统操作比较方便，查询速度也有所提升，
不过在麒麟系统上偶尔会出现页面显示异常。
""".strip()


success_count = 0
failure_count = 0

for number in range(1, 11):
    print(f"\n===== 第 {number}/10 次测试 =====")

    try:
        result = analyze_text(TEST_TEXT)
        success_count += 1

        print("状态：成功")
        print(f"情感：{result['sentiment']}")
        print(f"关键词：{'、'.join(result['keywords'])}")
        print(f"摘要：{result['summary']}")

    except Exception as error:
        failure_count += 1
        print("状态：失败")
        print(f"原因：{error}")


print("\n===== 测试统计 =====")
print(f"成功：{success_count} 次")
print(f"失败：{failure_count} 次")
print(f"JSON解析成功率：{success_count / 10:.0%}")
