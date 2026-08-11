# SQL 数据分析 Agent

自然语言转 SQL 的数据分析助手。输入问题，自动生成并执行 SQL，返回表格结果。

## 功能

- **自然语言转 SQL**：DeepSeek 自动生成查询语句
- **安全校验**：双重保护——只放行 SELECT + 拦截危险关键字和注入
- **自动纠错**：SQL 执行失败时自动让 LLM 修正重试
- **Web 界面**：浏览器直接查询，结果以表格展示

## 技术栈

| 组件 | 技术 |
|---|---|
| 数据库 | SQLite (in-memory → persistent) |
| LLM | DeepSeek V4 Flash（OpenAI 兼容） |
| 后端 | FastAPI |
| 前端 | 原生 HTML/CSS/JS |
| 校验 | 白名单（仅 SELECT）+ 黑名单（关键字/符号） |

## 数据库结构

5 张表：departments, employees, products, orders, order_items

含 8 个部门/员工、8 个产品、10 个订单、17 条订单明细的示例数据。

## 设计决策

- **SQL 生成与执行分离**：LLM 只负责生成，系统负责校验、执行、纠错
- **安全优先**：禁止 DDL/DML，拦截分号防止堆叠查询，最多重试 1 次
- **LLM 与 Embedding 解耦**：和项目 1（RAG）一样，LLM 可替换，不影响执行层
- **纠错上限**：max_retries=1，防止无限循环消耗 token

## 快速开始

```bash
# 1. 配置环境变量
cp .env.example .env
# 或从项目 1 复制共用 .env

# 2. 安装依赖
pip install openai python-dotenv fastapi uvicorn

# 3. 初始化数据库
python db.py

# 4. 启动服务
python -m uvicorn server:app --host 127.0.0.1 --port 8001
```

打开 http://127.0.0.1:8001 开始查询。

## 评测指标

| 指标 | 说明 |
|---|---|
| SQL 执行成功率 | LLM 生成 SQL 是否可执行 |
| 危险 SQL 拦截率 | validator 是否正确阻止非法操作 |
| 纠错成功率 | 重试机制是否成功修复 SQL 错误 |
| 平均响应时间 | 自然语言到结果的端到端延迟 |
