"""自然语言转 SQL：调用 DeepSeek 生成 SELECT 语句。"""

import os
import re
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

# 数据库 schema，告诉 LLM 表结构和示例数据
SCHEMA = """
表: departments (id, name)
  示例: 1, '技术部'

表: employees (id, name, department_id, salary, hire_date)
  示例: 1, '张三', 1, 25000, '2022-03-15'

表: products (id, name, category, price, stock)
  示例: 1, '智能音箱', '硬件', 299, 150

表: orders (id, customer_name, order_date)
  示例: 1, '字节跳动', '2025-01-15'

表: order_items (id, order_id, product_id, quantity)
  示例: 1, 1, 3, 5

关系: employees.department_id -> departments.id
      order_items.order_id -> orders.id
      order_items.product_id -> products.id
"""


def generate_sql(question: str) -> str:
    """输入自然语言问题，返回 SQL 查询语句。"""
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),
        messages=[
            {
                "role": "system",
                "content": (
                    "你是 SQLite SQL 生成器。只输出一条 SELECT 语句，不要任何解释、注释或 markdown。\n\n"
                    f"数据库结构：\n{SCHEMA}\n\n"
                    "规则：\n"
                    "- 只生成 SELECT，禁止 INSERT/UPDATE/DELETE/DROP\n"
                    "- 不要包含分号以外的多余字符\n"
                    "- 表名和字段名使用英文\n"
                ),
            },
            {"role": "user", "content": question},
        ],
        temperature=0.1,
    )

    raw = response.choices[0].message.content.strip()
    # 提取第一个 SELECT 语句
    match = re.search(r"SELECT\s+.+", raw, re.IGNORECASE | re.DOTALL)
    return match.group(0).strip() if match else ""