"""Embedding：用 Chroma 自带模型把文本转成向量。"""

from chromadb.utils import embedding_functions

ef = embedding_functions.DefaultEmbeddingFunction()

def embed(texts: list[str]) -> list[list[float]]:
    return ef(texts)