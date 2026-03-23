
from __future__ import annotations

import json
import random
import re
import string
import time
from email import policy
from email.parser import BytesParser
from html import unescape
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    from curl_cffi import requests as curl_requests
except ImportError:
    curl_requests = None

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ============================================================
# Cloudflare Temp Email 配置（从 config.json 加载）
# ============================================================

_config_path = Path(__file__).parent / "config.json"
_conf: Dict[str, Any] = {}
if _config_path.exists():
    with _config_path.open("r", encoding="utf-8") as _f:
        _conf = json.load(_f)

TEMP_MAIL_API_BASE = str(
    _conf.get("temp_mail_api_base")
    or _conf.get("duckmail_api_base")
    or ""
)
TEMP_MAIL_ADMIN_PASSWORD = str(
    _conf.get("temp_mail_admin_password")
    or _conf.get("duckmail_bearer")
    or ""
)
TEMP_MAIL_DOMAIN = str(_conf.get("temp_mail_domain", ""))
TEMP_MAIL_SITE_PASSWORD = str(_conf.get("temp_mail_site_password", ""))
PROXY = str(_conf.get("proxy", ""))

# ============================================================
# 适配层：为 DrissionPage_example.py 提供简单接口
# ============================================================

_temp_email_cache: Dict[str, str] = {}


def get_email_and_token() -> Tuple[Optional[str], Optional[str]]:
    """
    创建临时邮箱并返回 (email, mail_token)。
    供 DrissionPage_example.py 调用。
    """
    email, _password, mail_token = create_temp_email()
    if email and mail_token:
        _temp_email_cache[email] = mail_token
        return email, mail_token
    return None, None


def get_oai_code(dev_token: str, email: str, timeout: int = 30) -> Optional[str]:
    """
    轮询收件箱获取 OTP 验证码。
    供 DrissionPage_example.py 调用。

    Returns:
        验证码字符串（去除连字符，如 "MM0SF3"）或 None
    """
    code = wait_for_verification_code(mail_token=dev_token, timeout=timeout)
    if code:
        code = code.replace("-", "")
    return code


# ============================================================
# Cloudflare Temp Email 核心函数
# ============================================================

def _create_session():
    """创建请求会话（优先 curl_cffi）。"""
    if curl_requests:
        session = curl_requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json",
        })
        if PROXY:
            session.proxies = {"http": PROXY, "https": PROXY}
        return session, True

    s = requests.Session()
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json",
    })
    if PROXY:
        s.proxies = {"http": PROXY, "https": PROXY}
    return s, False


def _do_request(session, use_cffi, method, url, **kwargs):
    """统一请求，curl_cffi 自动附带 impersonate。"""
    if use_cffi:
        kwargs.setdefault("impersonate", "chrome131")
    return getattr(session, method)(url, **kwargs)


def _build_headers(extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    headers: Dict[str, str] = {}
    if TEMP_MAIL_SITE_PASSWORD:
        headers["x-custom-auth"] = TEMP_MAIL_SITE_PASSWORD
    if extra:
        headers.update(extra)
    return headers


def _generate_local_part(length: int = 10) -> str:
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def create_temp_email() -> Tuple[str, str, str]:
    """创建 Cloudflare Temp Email 地址，返回 (email, password, mail_token)。"""
    if not TEMP_MAIL_API_BASE:
        raise Exception("temp_mail_api_base 未设置，无法创建临时邮箱")
    if not TEMP_MAIL_ADMIN_PASSWORD:
        raise Exception("temp_mail_admin_password 未设置，无法创建临时邮箱")
    if not TEMP_MAIL_DOMAIN:
        raise Exception("temp_mail_domain 未设置，无法创建临时邮箱")

    api_base = TEMP_MAIL_API_BASE.rstrip("/")
    email_local = _generate_local_part(random.randint(8, 12))
    session, use_cffi = _create_session()
    headers = _build_headers({"x-admin-auth": TEMP_MAIL_ADMIN_PASSWORD})

    try:
        res = _do_request(
            session,
            use_cffi,
            "post",
            f"{api_base}/admin/new_address",
            json={
                "name": email_local,
                "domain": TEMP_MAIL_DOMAIN,
                "enablePrefix": False,
            },
            headers=headers,
            timeout=20,
        )
        if res.status_code != 200:
            raise Exception(f"创建邮箱失败: {res.status_code} - {res.text[:200]}")

        data = res.json()
        email = data.get("address") or ""
        mail_token = data.get("jwt") or ""
        password = data.get("password") or ""
        if not email or not mail_token:
            raise Exception(f"接口返回缺少 address/jwt: {data}")

        print(f"[*] Cloudflare 临时邮箱创建成功: {email}")
        return email, password, mail_token
    except Exception as e:
        raise Exception(f"Cloudflare 临时邮箱创建失败: {e}")


def fetch_emails(mail_token: str) -> List[Dict[str, Any]]:
    """获取邮件列表。"""
    try:
        api_base = TEMP_MAIL_API_BASE.rstrip("/")
        headers = _build_headers({"Authorization": f"Bearer {mail_token}"})
        session, use_cffi = _create_session()
        res = _do_request(
            session,
            use_cffi,
            "get",
            f"{api_base}/api/mails",
            params={"limit": 20, "offset": 0},
            headers=headers,
            timeout=20,
        )
        if res.status_code == 200:
            data = res.json()
            if isinstance(data, dict):
                return data.get("results") or data.get("data") or []
    except Exception:
        pass
    return []


def fetch_email_detail(mail_token: str, msg_id: str) -> Optional[Dict[str, Any]]:
    """获取单封邮件详情。"""
    try:
        api_base = TEMP_MAIL_API_BASE.rstrip("/")
        headers = _build_headers({"Authorization": f"Bearer {mail_token}"})
        session, use_cffi = _create_session()
        res = _do_request(
            session,
            use_cffi,
            "get",
            f"{api_base}/api/mail/{msg_id}",
            headers=headers,
            timeout=20,
        )
        if res.status_code == 200:
            data = res.json()
            if isinstance(data, dict):
                return data
    except Exception:
        pass
    return None


def wait_for_verification_code(mail_token: str, timeout: int = 120) -> Optional[str]:
    """轮询临时邮箱，等待验证码邮件。"""
    start = time.time()
    seen_ids = set()

    while time.time() - start < timeout:
        messages = fetch_emails(mail_token)
        for msg in messages:
            if not isinstance(msg, dict):
                continue
            msg_id = msg.get("id")
            if not msg_id or msg_id in seen_ids:
                continue
            seen_ids.add(msg_id)

            detail = fetch_email_detail(mail_token, str(msg_id))
            if not detail:
                continue

            content = _extract_mail_content(detail)
            code = extract_verification_code(content)
            if code:
                print(f"[*] 从 Cloudflare 临时邮箱提取到验证码: {code}")
                return code
        time.sleep(3)
    return None


def _extract_mail_content(detail: Dict[str, Any]) -> str:
    """兼容 text/html/raw MIME 三种内容来源。"""
    direct_parts = [
        detail.get("subject"),
        detail.get("text"),
        detail.get("html"),
        detail.get("raw"),
        detail.get("source"),
    ]
    direct_content = "\n".join(str(part) for part in direct_parts if part)
    if detail.get("text") or detail.get("html"):
        return direct_content

    raw = detail.get("raw") or detail.get("source")
    if not raw or not isinstance(raw, str):
        return direct_content
    return f"{direct_content}\n{_parse_raw_email(raw)}"


def _parse_raw_email(raw: str) -> str:
    try:
        message = BytesParser(policy=policy.default).parsebytes(raw.encode("utf-8", errors="ignore"))
    except Exception:
        return raw

    parts: List[str] = []
    subject = message.get("subject")
    if subject:
        parts.append(f"Subject: {subject}")

    if message.is_multipart():
        for part in message.walk():
            if part.get_content_maintype() == "multipart":
                continue
            disposition = (part.get_content_disposition() or "").lower()
            if disposition == "attachment":
                continue
            content = _decode_email_part(part)
            if content:
                parts.append(content)
    else:
        content = _decode_email_part(message)
        if content:
            parts.append(content)
    return "\n".join(parts)


def _decode_email_part(part) -> str:
    try:
        content = part.get_content()
        if isinstance(content, bytes):
            charset = part.get_content_charset() or "utf-8"
            content = content.decode(charset, errors="ignore")
        if not isinstance(content, str):
            content = str(content)
        if "html" in (part.get_content_type() or "").lower():
            content = _html_to_text(content)
        return content.strip()
    except Exception:
        payload = part.get_payload(decode=True)
        if isinstance(payload, bytes):
            charset = part.get_content_charset() or "utf-8"
            return payload.decode(charset, errors="ignore").strip()
    return ""


def _html_to_text(html: str) -> str:
    text = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", html)
    text = re.sub(r"(?i)<br\s*/?>", "\n", text)
    text = re.sub(r"(?i)</p>", "\n", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return unescape(re.sub(r"[ \t\r\f\v]+", " ", text)).strip()


def extract_verification_code(content: str) -> Optional[str]:
    """
    从邮件内容提取验证码。
    Grok/x.ai 格式：MM0-SF3（3位-3位字母数字混合）或 6 位纯数字。
    """
    if not content:
        return None

    # 模式 1: Grok 格式 XXX-XXX
    m = re.search(r"(?<![A-Z0-9-])([A-Z0-9]{3}-[A-Z0-9]{3})(?![A-Z0-9-])", content)
    if m:
        return m.group(1)

    # 模式 2: 带标签的验证码
    m = re.search(r"(?:verification code|验证码|your code)[:\s]*[<>\s]*([A-Z0-9]{3}-[A-Z0-9]{3})\b", content, re.IGNORECASE)
    if m:
        return m.group(1)

    # 模式 3: HTML 样式包裹
    m = re.search(r"background-color:\s*#F3F3F3[^>]*>[\s\S]*?([A-Z0-9]{3}-[A-Z0-9]{3})[\s\S]*?</p>", content)
    if m:
        return m.group(1)

    # 模式 4: Subject 行 6 位数字
    m = re.search(r"Subject:.*?(\d{6})", content)
    if m and m.group(1) != "177010":
        return m.group(1)

    # 模式 5: HTML 标签内 6 位数字
    for code in re.findall(r">\s*(\d{6})\s*<", content):
        if code != "177010":
            return code

    # 模式 6: 独立 6 位数字
    for code in re.findall(r"(?<![&#\d])(\d{6})(?![&#\d])", content):
        if code != "177010":
            return code

    return None
