# AI 应用开发作品集

三个 AI 应用项目，`docker compose up` 一键启动。

## 项目列表

### 1. RAG 求职知识库助手

基于 Chroma + DeepSeek 的检索增强生成问答系统。30 篇技术文档，语义检索 + 来源引用。

| 指标 | 数值 |
|---|---|
| 检索命中率 | 87.5% |
| 平均响应时间 | 279ms |
| 文档数 | 30 篇 / 132 chunks |

→ [详细 README](./project-1-rag-assistant/README.md)

### 2. SQL 数据分析 Agent

自然语言转 SQL，集成安全校验与自动纠错。双保险策略：仅放行 SELECT + 拦截危险关键字。

→ [详细 README](./project-2-sql-agent/README.md)

### 3. 简历与 JD 匹配助手

输入简历和 JD，LLM 输出结构化 MatchReport：匹配分数、缺口技能、项目补强建议、面试风险点。

→ [详细 README](./project-3-jd-match/README.md)

## 一键启动

```bash
docker compose up --build
```

| 服务 | 地址 |
|---|---|
| RAG 知识库 | http://127.0.0.1:8010 |
| SQL Agent | http://127.0.0.1:8011 |
| JD 匹配 | http://127.0.0.1:8012 |

启动后初始化数据：

```bash
docker compose exec rag python ingest.py
docker compose exec sql python db.py
```

## 技术栈

Python · FastAPI · Chroma · SQLite · Docker · DeepSeek API (OpenAI 兼容)

## 仓库结构

```
├── docker-compose.yml              # 统一编排
├── project-1-rag-assistant/        # RAG 知识库
├── project-2-sql-agent/            # SQL Agent
└── project-3-jd-match/             # JD 匹配
```
