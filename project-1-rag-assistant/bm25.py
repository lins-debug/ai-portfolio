"""BM25 关键词检索：精确匹配专业名词，和向量检索互补。"""

import math
from collections import Counter
from pathlib import Path

from chunker import chunk_markdown

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"


def tokenize(text: str) -> list[str]:
    """英文按词切，中文按连续双字切（和 rag_index 一致）。"""
    tokens: list[str] = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch.isascii() and (ch.isalnum() or ch == "_"):
            j = i + 1
            while j < len(text) and text[j].isascii() and (text[j].isalnum() or text[j] == "_"):
                j += 1
            tokens.append(text[i:j].lower())
            i = j
        elif "\u4e00" <= ch <= "\u9fff":
            if i + 1 < len(text) and "\u4e00" <= text[i + 1] <= "\u9fff":
                tokens.append(text[i:i+2])
            else:
                tokens.append(ch)
            i += 1
        else:
            i += 1
    return tokens


def build_chunks() -> list[dict]:
    """从 data/ 读取所有 md，切成 chunk（和 ingest.py 同一套逻辑）。"""
    chunks: list[dict] = []
    for path in sorted(DATA_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        chunks.extend(chunk_markdown(text, path.name))
    return chunks


class BM25Index:
    """内存版 BM25 索引，适合小规模文档。"""

    def __init__(self, chunks: list[dict] | None = None, k1: float = 1.5, b: float = 0.75):
        if chunks is None:
            chunks = build_chunks()
        self.chunks = chunks
        self.k1 = k1
        self.b = b
        self.doc_lens: list[int] = []
        self.term_freqs: list[Counter] = []
        self.doc_freq: Counter[str] = Counter()
        self.n = len(chunks)

        for chunk in chunks:
            tokens = tokenize(chunk["text"])
            self.doc_lens.append(len(tokens))
            tf = Counter(tokens)
            self.term_freqs.append(tf)
            for term in tf:
                self.doc_freq[term] += 1

        self.avg_len = sum(self.doc_lens) / max(self.n, 1)

    def _idf(self, term: str) -> float:
        df = self.doc_freq.get(term, 0)
        return math.log((self.n - df + 0.5) / (df + 0.5) + 1)

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """返回按 BM25 分数排序的 chunk 列表。"""
        q_terms = tokenize(query)
        scored: list[tuple[float, dict]] = []

        for i, chunk in enumerate(self.chunks):
            score = 0.0
            for term in q_terms:
                tf = self.term_freqs[i].get(term, 0)
                if tf == 0:
                    continue
                idf = self._idf(term)
                dl = self.doc_lens[i]
                denom = tf + self.k1 * (1 - self.b + self.b * dl / self.avg_len)
                score += idf * tf * (self.k1 + 1) / denom
            if score > 0:
                scored.append((score, chunk))

        scored.sort(key=lambda item: item[0], reverse=True)
        return [
            {
                "id": chunk["id"],
                "text": chunk["text"],
                "metadata": {"source": chunk["source"], "title": chunk["title"]},
                "bm25_score": round(score, 4),
            }
            for score, chunk in scored[:top_k]
        ]