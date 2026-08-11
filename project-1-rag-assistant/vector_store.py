"""封装 Chroma 向量存储：建表、写入、检索。"""

from pathlib import Path

from chromadb import PersistentClient

from embedder import ef

ROOT = Path(__file__).resolve().parent
DB_DIR = str(ROOT / "chroma_db")
COLLECTION_NAME = "rag_assistant"


def get_collection():
    """获取或创建 Collection。"""
    client = PersistentClient(path=DB_DIR)
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef,
    )


def add_chunks(chunks: list[dict]):
    """把 chunk 列表写入向量库。"""
    col = get_collection()
    col.add(
        ids=[c["id"] for c in chunks],
        documents=[c["text"] for c in chunks],
        metadatas=[{"source": c["source"], "title": c["title"]} for c in chunks],
    )


def search(question: str, top_k: int = 3) -> list[dict]:
    """按问题检索最相似的 chunk。"""
    col = get_collection()
    results = col.query(query_texts=[question], n_results=top_k)

    out = []
    if results["ids"] and results["ids"][0]:
        for i in range(len(results["ids"][0])):
            out.append({
                "id": results["ids"][0][i],
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
            })
    return out
