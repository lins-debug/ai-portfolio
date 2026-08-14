"""混合检索：向量 + BM25 → RRF 融合重排序。"""

from bm25 import BM25Index
from vector_store import search as vector_search

RRF_K = 60  # RRF 常数，控制排名权重
_BM25 = BM25Index()  # 模块级缓存：程序启动时只建一次索引

def _rrf_score(rank: int) -> float:
    """单个检索器里第 rank 名的文档得分。"""
    return 1.0 / (RRF_K + rank + 1)


def hybrid_search(question: str, top_k: int = 3) -> list[dict]:
    """融合向量检索和 BM25，返回 top_k 个 chunk。"""
    # 1. 两个检索器各取 top 10
    vector_results = vector_search(question, top_k * 4)
    bm25_results = _BM25.search(question, top_k * 4)
    # 2. RRF 融合：每个文档累加两个检索器里的排名分
    fused: dict[str, dict] = {}
    for rank, item in enumerate(vector_results):
        doc_id = item["id"]
        score = _rrf_score(rank)
        fused.setdefault(doc_id, item)["rrf_score"] = fused.get(doc_id, {}).get("rrf_score", 0) + score
        fused.setdefault(doc_id, item)["vector_rank"] = rank

    for rank, item in enumerate(bm25_results):
        doc_id = item["id"]
        fused.setdefault(doc_id, item)["rrf_score"] = fused.get(doc_id, {}).get("rrf_score", 0) + _rrf_score(rank)
        fused.setdefault(doc_id, item)["bm25_rank"] = rank

    # 3. 按融合分排序，按 source 去重，取 top_k
    ranked = sorted(fused.values(), key=lambda x: x["rrf_score"], reverse=True)
    seen_sources: set[str] = set()
    out = []
    for item in ranked:
        source = item["metadata"]["source"]
        if source in seen_sources:
            continue
        seen_sources.add(source)
        out.append(item)
        if len(out) >= top_k:
            break

    return out


# 让原 retriever 无痛切换：hybrid_search 提供和 search 一样的接口
search = hybrid_search