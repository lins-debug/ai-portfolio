# AI 应用开发作品集

三个 AI 应用项目，`docker compose up --build` 一键启动。

## 项目总览

| 项目 | 说明 | 核心技术 |
|---|---|---|
| RAG 求职知识库 | 30 篇文档语义检索 + LLM 问答 | Chroma、embedding、DeepSeek |
| SQL 数据分析 Agent | 自然语言转 SQL + 安全校验 | SQLite、白名单/黑名单、自动纠错 |
| JD 匹配助手 | 简历 vs JD 结构化匹配分析 | DeepSeek、JSON Schema 约束 |

## 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/lins-debug/ai-portfolio.git
cd ai-portfolio

# 2. 配置 API Key
# 在 project-1-rag-assistant/ 下把 .env.example 复制一份，填上你的 API Key
cp project-1-rag-assistant/.env.example project-1-rag-assistant/.env
# 编辑 .env，把 sk-your-key-here 替换成真实 key

# 3. 一键启动全部服务
docker compose up --build
```

启动后访问：

| 服务 | 地址 |
|---|---|
| RAG 知识库提问 | http://127.0.0.1:8010 |
| SQL Agent 查询 | http://127.0.0.1:8011 |
| JD 匹配分析 | http://127.0.0.1:8012 |

> 如果跳过第 2 步，`docker compose up` 也能启动（用 `.env.example` 占位值），但实际提问会因为没有真实 API Key 而报错。

## 初始化数据

服务启动后，需要往 RAG 知识库灌文档、给 SQL Agent 建数据表：

```bash
docker compose exec rag python ingest.py
docker compose exec sql python db.py
```

## 项目详情

每个项目都有独立的 README：

- [RAG 求职知识库助手](./project-1-rag-assistant/README.md) — 检索命中率 87.5%，平均响应 279ms
- [SQL 数据分析 Agent](./project-2-sql-agent/README.md) — 自然语言转 SQL，安全校验 + 自动纠错
- [JD 匹配助手](./project-3-jd-match/README.md) — 结构化 MatchReport，多岗位对比

## 技术栈

Python · FastAPI · Chroma · SQLite · Docker · DeepSeek API (OpenAI 兼容)

## 仓库结构

```
├── docker-compose.yml              # 统一编排，一键启动
├── project-1-rag-assistant/        # RAG 知识库
├── project-2-sql-agent/            # SQL Agent
└── project-3-jd-match/             # JD 匹配
```
