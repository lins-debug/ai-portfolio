# 向量数据库

## 向量数据库的用途

专门存储和检索高维向量的数据库。核心能力是近似最近邻搜索，在毫秒级从百万向量中找到最相似的 top-k 个。

## Chroma

Chroma 是轻量级开源向量数据库，适合学习和中小规模项目。特点：Python 原生 API、支持多种 embedding 函数、持久化存储、简单易用。

## 其他常见向量数据库

Pinecone：全托管云服务，无需运维
Weaviate：开源，支持 GraphQL 接口
Milvus：高性能分布式向量数据库
Qdrant：Rust 编写，性能优秀
FAISS：Facebook 的向量检索库，非完整数据库

## 选型考虑

学习阶段用 Chroma 足够。生产环境考虑：数据规模、QPS、托管还是自建、是否需过滤检索、embedding 集成方式。Chroma 适合 10 万级向量以下的场景。

