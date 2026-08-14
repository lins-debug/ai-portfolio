"""检索：混合检索（向量 + BM25 + RRF 融合）。"""

from hybrid import hybrid_search


def retrieve(question: str, top_k: int = 3) -> list[dict]:
    """输入问题，返回最相关的 top_k 个 chunk。"""
    return hybrid_search(question, top_k)