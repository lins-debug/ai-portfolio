"""检索：把问题变成相关 chunk 列表。"""

from vector_store import search


def retrieve(question: str, top_k: int = 3) -> list[dict]:
    """输入问题，返回最相关的 top_k 个 chunk（按 source 去重）。"""
    results = search(question, top_k * 2)

    seen_sources: dict[str, dict] = {}
    for item in results:
        source = item["metadata"]["source"]
        if source not in seen_sources:
            seen_sources[source] = item

    return list(seen_sources.values())[:top_k]
