# Embedding 向量嵌入

## 什么是 Embedding

Embedding 是将文本转换为固定长度向量的技术。语义相近的文本，向量在空间中也更接近。向量维度从几十到几千不等，OpenAI 的 text-embedding-3-small 是 1536 维。

## 相似度度量

余弦相似度：衡量两个向量方向的接近程度，范围 [-1, 1]，RAG 中最常用
欧氏距离：两点间的直线距离，越小越相似
点积：未归一化时受向量大小影响

## Embedding 模型选择

商业 API：OpenAI text-embedding-3-small/large、Cohere embed
开源模型：BGE、all-MiniLM-L6-v2、text2vec-large-chinese
选择考虑：中英文支持、维度、推理速度、成本

## 实践注意事项

输入文本预处理很重要：去噪、截断过长文本
同一问题时，中文embedding应考虑分词和语义层面的对齐
embedding 模型的选择直接影响检索质量，是最关键的设计决策之一