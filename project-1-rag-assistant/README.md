# RAG 求职知识库助手

基于检索增强生成（RAG）的求职知识库问答系统。支持 30 篇技术文档的语义检索，结合 LLM 生成带来源引用的答案。

## 功能

- **文档管理**：支持 Markdown 文档按标题自动切分入库
- **向量检索**：基于 Chroma 向量数据库的语义搜索
- **答案生成**：结合检索结果调用 LLM 生成答案
- **来源引用**：每个答案附带来源文档和章节引用
- **API 服务**：FastAPI 提供 `/ask` 接口
- **Web 前端**：浏览器直接使用的交互界面

## 技术栈

| 组件 | 技术 |
|---|---|
| 切分 | 自定义标题级 chunker |
| Embedding | all-MiniLM-L6-v2 (384d，本地运行) |
| 向量库 | Chroma (PersistentClient) |
| LLM | DeepSeek V4 Flash（OpenAI 兼容接口） |
| 后端 | FastAPI + uvicorn |
| 前端 | 原生 HTML/CSS/JS |

## 设计决策

- **LLM 与 Embedding 解耦**：答案生成用 DeepSeek API，文本向量化用本地模型，互不依赖
- **为什么用 all-MiniLM-L6-v2**：免费、本地运行、384 维轻量，适合中英混合文档场景
- **为什么兼容 OpenAI SDK**：DeepSeek API 与 OpenAI 接口兼容，切换模型只需改环境变量

## 快速开始

```bash
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env，填入你的 API Key

# 5. 入库文档
python ingest.py

# 6. 启动服务
python -m uvicorn server:app --host 127.0.0.1 --port 8000
```

打开 http://127.0.0.1:8000 开始提问。

## CLI 查询

```bash
python query.py "什么是 RAG？"
python query.py "Python GIL 是什么？" --no-llm  # 只看检索结果
```

## 评测指标

| 指标 | 数值 |
|---|---|
| 检索命中率 | 87.5% (7/8) |
| 来源引用完整率 | 100% |
| 平均响应时间 | 279ms |
| Faithfulness | 33.3% |

运行评测：`python eval.py`

## 项目结构

```
├── data/               # 30 篇 Markdown 文档
├── chunker.py          # 文档切分
├── embedder.py         # Embedding 封装
├── vector_store.py     # Chroma 向量库封装
├── retriever.py        # 检索入口
├── generator.py        # LLM 答案生成
├── ingest.py           # 一键入库
├── query.py            # CLI 查询
├── server.py           # FastAPI 服务
├── eval.py             # 评测脚本
└── static/index.html   # 前端页面
```
