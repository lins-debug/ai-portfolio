"""SQL 执行器：校验 + 执行 + 自动纠错。"""

from db import get_connection
from generator import generate_sql
from validator import validate


def execute(question: str, max_retries: int = 1) -> dict:
    """自然语言 → SQL → 校验 → 执行 → 返回结果。

    返回格式统一：{"sql": str, "columns": [...], "rows": [...], "error": str|null}
    """
    sql = generate_sql(question)
    sql = sql.rstrip(';').strip()  # 去除 LLM 自动加的末尾分号
    for attempt in range(max_retries + 1):
        # 第一关：安全校验
        ok, reason = validate(sql)
        if not ok:
            return {"sql": sql, "columns": [], "rows": [], "error": f"安全检查失败: {reason}"}

        # 第二关：执行
        conn = get_connection()
        try:
            cur = conn.execute(sql)
            columns = [desc[0] for desc in cur.description] if cur.description else []
            rows = [list(row) for row in cur.fetchall()]
            conn.close()
            return {"sql": sql, "columns": columns, "rows": rows, "error": None}
        except Exception as e:
            conn.close()
            if attempt < max_retries:
                # 第三关：让 LLM 修正 SQL
                sql = generate_sql(
                    f"以下 SQL 执行报错: {e}\n请修正:\n{sql}\n原始问题: {question}"
                )
            else:
                return {"sql": sql, "columns": [], "rows": [], "error": str(e)}

    return {"sql": sql, "columns": [], "rows": [], "error": "重试失败"}