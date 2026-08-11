"""SQL 安全校验：只放行安全的 SELECT 语句。"""

import re

# 黑名单：即使 SELECT 也禁止包含这些
FORBIDDEN_KEYWORDS = [
    "DROP", "DELETE", "INSERT", "UPDATE",
    "ATTACH", "DETACH", "ALTER", "PRAGMA",
    "VACUUM", "REINDEX",
]

# 黑名单：禁止的关键符号（防止 SQL 注入）
FORBIDDEN_SYMBOLS = ["--", "/*", "*/", ";"]


def validate(sql: str) -> tuple[bool, str]:
    """校验 SQL 是否安全。返回 (是否安全, 原因)。"""
    if not sql:
        return False, "SQL 为空"

    # 白名单：必须以 SELECT 开头
    if not sql.upper().lstrip().startswith("SELECT"):
        return False, "只允许 SELECT 查询"

    # 黑名单：检查危险关键字
    upper = sql.upper()
    for kw in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{kw}\b", upper):
            return False, f"禁止使用 {kw}"

    # 黑名单：检查危险符号
    for sym in FORBIDDEN_SYMBOLS:
        if sym in sql:
            return False, f"禁止使用 '{sym}'"

    return True, "OK"