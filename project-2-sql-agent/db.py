"""SQLite 数据库初始化：建表 + 填充示例数据。"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "company.db"


def init_db():
    """创建表结构并填充假数据。首次调用时初始化。"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    # ── 建表 ──
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department_id INTEGER REFERENCES departments(id),
            salary REAL NOT NULL,
            hire_date TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            customer_name TEXT NOT NULL,
            order_date TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY,
            order_id INTEGER REFERENCES orders(id),
            product_id INTEGER REFERENCES products(id),
            quantity INTEGER NOT NULL
        );
    """)

    # ── 灌数据（只在表为空时） ──
    cur.execute("SELECT COUNT(*) FROM departments")
    if cur.fetchone()[0] == 0:
        cur.executescript("""
            INSERT INTO departments VALUES (1, '技术部');
            INSERT INTO departments VALUES (2, '产品部');
            INSERT INTO departments VALUES (3, '市场部');
            INSERT INTO departments VALUES (4, '人事部');

            INSERT INTO employees VALUES (1, '张三', 1, 25000, '2022-03-15');
            INSERT INTO employees VALUES (2, '李四', 1, 22000, '2023-01-10');
            INSERT INTO employees VALUES (3, '王五', 1, 28000, '2021-07-01');
            INSERT INTO employees VALUES (4, '赵六', 2, 20000, '2023-06-20');
            INSERT INTO employees VALUES (5, '孙七', 2, 18000, '2024-02-01');
            INSERT INTO employees VALUES (6, '周八', 3, 19000, '2022-11-05');
            INSERT INTO employees VALUES (7, '吴九', 3, 17000, '2024-05-15');
            INSERT INTO employees VALUES (8, '郑十', 4, 16000, '2023-09-01');

            INSERT INTO products VALUES (1, '智能音箱', '硬件', 299, 150);
            INSERT INTO products VALUES (2, '蓝牙耳机', '硬件', 199, 300);
            INSERT INTO products VALUES (3, '数据分析平台', '软件', 999, 50);
            INSERT INTO products VALUES (4, '项目管理 SaaS', '软件', 499, 80);
            INSERT INTO products VALUES (5, 'AI 客服机器人', 'AI', 1999, 20);
            INSERT INTO products VALUES (6, 'RAG 知识库引擎', 'AI', 2999, 10);
            INSERT INTO products VALUES (7, '在线课程订阅', '内容', 99, 500);
            INSERT INTO products VALUES (8, '技术白皮书', '内容', 29, 1000);

            INSERT INTO orders VALUES (1, '字节跳动', '2025-01-15');
            INSERT INTO orders VALUES (2, '阿里巴巴', '2025-01-20');
            INSERT INTO orders VALUES (3, '腾讯科技', '2025-02-10');
            INSERT INTO orders VALUES (4, '美团', '2025-02-15');
            INSERT INTO orders VALUES (5, '字节跳动', '2025-03-01');
            INSERT INTO orders VALUES (6, '拼多多', '2025-03-05');
            INSERT INTO orders VALUES (7, '阿里巴巴', '2025-04-01');
            INSERT INTO orders VALUES (8, '腾讯科技', '2025-04-15');
            INSERT INTO orders VALUES (9, '华为技术', '2025-05-01');
            INSERT INTO orders VALUES (10, '字节跳动', '2025-05-10');

            INSERT INTO order_items VALUES (1, 1, 3, 5);
            INSERT INTO order_items VALUES (2, 1, 5, 2);
            INSERT INTO order_items VALUES (3, 2, 1, 10);
            INSERT INTO order_items VALUES (4, 2, 2, 15);
            INSERT INTO order_items VALUES (5, 3, 4, 3);
            INSERT INTO order_items VALUES (6, 3, 6, 1);
            INSERT INTO order_items VALUES (7, 4, 2, 20);
            INSERT INTO order_items VALUES (8, 5, 3, 2);
            INSERT INTO order_items VALUES (9, 5, 5, 1);
            INSERT INTO order_items VALUES (10, 6, 7, 50);
            INSERT INTO order_items VALUES (11, 7, 6, 2);
            INSERT INTO order_items VALUES (12, 7, 1, 5);
            INSERT INTO order_items VALUES (13, 8, 4, 4);
            INSERT INTO order_items VALUES (14, 9, 3, 3);
            INSERT INTO order_items VALUES (15, 9, 2, 10);
            INSERT INTO order_items VALUES (16, 10, 5, 2);
            INSERT INTO order_items VALUES (17, 10, 6, 1);
        """)

    conn.commit()
    conn.close()
    print(f"数据库已初始化: {DB_PATH}")


def get_connection() -> sqlite3.Connection:
    """获取数据库连接。"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row  # 让结果能用列名访问
    return conn


if __name__ == "__main__":
    init_db()