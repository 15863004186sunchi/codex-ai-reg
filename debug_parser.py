import re
import json

def _extract_otp_code(content: str) -> str:
    if not content:
        return ""
    patterns = [
        r"(?i)Your ChatGPT code is\s*(\d{6})",
        r"(?i)ChatGPT code is\s*(\d{6})",
        r"(?i)verification code to continue:\s*(\d{6})",
        r"(?i)Subject:.*?(\d{6})",
    ]
    for p in patterns:
        m = re.search(p, content)
        if m:
            return m.group(1)
    fallback = re.search(r"(?<!\d)(\d{6})(?!\d)", content)
    return fallback.group(1) if fallback else ""

def test_logic(text_content):
    print(f"Testing with: {repr(text_content)}")
    # 模拟 _fetch_code 内部逻辑
    try:
        data = json.loads(text_content)
        if isinstance(data, list) and data:
            entry = data[0]
            code = str(entry.get("verification_code") or "").strip()
            if not code:
                code = _extract_otp_code(str(entry.get("text", "")) + "\n" + str(entry.get("subject", "")))
            print(f"JSON List Branch code: {code}")
            return code
    except Exception as e:
        print(f"JSON Parse Exception: {e}")
        pass
    
    # 当前 Bug 就在这里：如果 JSON 解析成功(如纯数字)但不是 List，就会跳过下面的逻辑直接返回空
    # 修复应该是：不管 JSON 解析成什么，如果没有拿到 code，就用正则扫一遍 text
    res_code = _extract_otp_code(text_content)
    print(f"Fallback Regex code: {res_code}")
    return res_code

#Case 1: 纯文本数字 (MailAPI.ICU type=code 可能返回的结果)
test_logic("297962")

#Case 2: 带有 HTML 标签的数字
test_logic("<html><body><pre>747217</pre></body></html>")

#Case 3: 标准 JSON List
test_logic('[{"verification_code": "112233"}]')
