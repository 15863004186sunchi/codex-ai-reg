"""
测试脚本: 验证 MailAPI.ICU 能否正常取到验证码 (Bugfix 版)
用法:
  python test_mailapi_icu.py "xxx@hotmail.com----https://mailapi.icu/key?type=html&orderNo=xxxx"
"""

import sys
import re
import time
import requests
import urllib.parse as urlparse

# ── 配置 ─────────────────────────────────────────────────────────────────────
POLL_INTERVAL = 5    # 轮询间隔（秒）
MAX_RETRIES   = 20   # 最大轮询次数

# ── 参数解析 ─────────────────────────────────────────────────────────────────
if len(sys.argv) < 2:
    print("用法: python test_mailapi_icu.py \"email----api_url\"")
    sys.exit(1)

account_str = sys.argv[1].strip()
parts = account_str.split("----")
if len(parts) < 2:
    print("[ERROR] 格式错误，必须是 email----api_url")
    sys.exit(1)

email, api_url = parts[0].strip(), parts[1].strip()

# ── 转换 URL ───────────────────────────────────────────────────────────────────
parsed = urlparse.urlparse(api_url)
qs = urlparse.parse_qs(parsed.query, keep_blank_values=True)
qs["type"] = ["code"]
new_query = urlparse.urlencode({k: v[0] for k, v in qs.items()})
code_url = urlparse.urlunparse(parsed._replace(query=new_query))

print(f"\n{'='*60}")
print(f"  邮箱   : {email}")
print(f"  取码URL: {code_url}")
print(f"{'='*60}\n")


def extract_otp(text: str) -> str:
    """从文本或 HTML 中提取 6 位数字验证码"""
    # 提取所有 6 位数字
    m = re.findall(r'\b(\d{6})\b', text)
    return m[0] if m else ""


# ── 轮询 ───────────────────────────────────────────────────────────────────────
for attempt in range(1, MAX_RETRIES + 1):
    # 模拟项目逻辑: 先尝试代理 (此处脚本简化为直连，因为用户手动测试能通)
    # 在项目中我们增加了 Retry-Direct 策略
    try:
        resp = requests.get(code_url, timeout=12)
        print(f"[{attempt}/{MAX_RETRIES}] 状态码: {resp.status_code}")

        if resp.status_code == 200:
            print(f"         原始文本: {resp.text.strip()}")
            
            # 1. 尝试 JSON
            code = ""
            try:
                data = resp.json()
                if isinstance(data, list) and data:
                    entry = data[0]
                    code = str(entry.get("verification_code") or "").strip()
                    if not code:
                        code = extract_otp(str(entry.get("text", "")) + "\n" + str(entry.get("subject", "")))
            except:
                pass

            # 2. 正则兜底 (适配针对 HTML <pre>747217</pre> 的情况)
            if not code:
                code = extract_otp(resp.text)
                if code:
                    print(f"         [Regex] 从响应文本中成功提取验证码")

            if code:
                print(f"\n✅ 成功取到验证码: \033[32m{code}\033[0m")
                sys.exit(0)
            else:
                print("         响应正常但未找到 6 位验证码")

        elif resp.status_code == 404:
            print("         暂无邮件")
        else:
            print(f"         错误码: {resp.status_code}")

    except Exception as e:
        print(f"[{attempt}/{MAX_RETRIES}] 请求异常: {e}")

    if attempt < MAX_RETRIES:
        time.sleep(POLL_INTERVAL)

print("\n❌ 超时！")
