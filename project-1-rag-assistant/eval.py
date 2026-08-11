"""检索质量评测：命中率、Faithfulness、响应时间、来源完整率。"""

import time
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

import retriever
import generator

TEST_CASES = [
    ("什么是 RAG？", "05-rag-fundamentals.md"),
    ("什么是 embedding？", "06-embedding-guide.md"),
    ("Python GIL 是什么？", "02-python-interview.md"),
    ("什么是过拟合？", "03-ml-basics.md"),
    ("Chroma 是什么？", "07-vector-database.md"),
    ("Transformer 架构是什么？", "04-deep-learning.md"),
    ("向量数据库有哪些选择？", "07-vector-database.md"),
    ("Prompt 怎么写？", "10-prompt-engineering.md"),
]


def eval_retrieval():
    hit = 0
    total = 0
    times = []
    source_complete = 0

    for question, expected_file in TEST_CASES:
        total += 1
        start = time.perf_counter()
        results = retriever.retrieve(question, top_k=3)
        elapsed = time.perf_counter() - start
        times.append(elapsed)

        sources = [item["metadata"]["source"] for item in results]
        hit += 1 if expected_file in sources else 0

        for item in results:
            meta = item["metadata"]
            if meta.get("source") and meta.get("title"):
                source_complete += 1

        print(f"  {question}")
        print(f"    期望: {expected_file}  实际: {sources}")
        print(f"    {'✓ 命中' if expected_file in sources else '✗ 未命中'}  {elapsed:.3f}s")
        print()

    print(f"检索命中率: {hit}/{total} = {hit/total:.1%}")
    print(f"来源引用完整率: {source_complete}/{total*3} = {source_complete/(total*3):.1%}")
    print(f"平均响应时间: {sum(times)/len(times)*1000:.0f}ms")


def eval_faithfulness():
    """Faithfulness：检查答案与 chunk 的关键词重合度。"""
    print("=== Faithfulness 检查 ===")
    total_matched = 0
    total_chunks = 0

    for question, _ in TEST_CASES[:4]:
        results = retriever.retrieve(question, top_k=3)
        answer = generator.generate(question, results)

        matched = 0
        for item in results:
            # 把 chunk 文本拆成连续二字词
            text = item["text"]
            bigrams = {text[i:i+2] for i in range(len(text)-1)}
            if not bigrams:
                continue
            # 计算有多少比例的词在答案中出现了
            overlap = sum(1 for b in bigrams if b in answer) / len(bigrams)
            if overlap > 0.3:  # 超过 30% 重合就算引用了
                matched += 1

        total_matched += matched
        total_chunks += len(results)

        print(f"  {question}")
        print(f"    忠实引用: {matched}/{len(results)}")
        print()

    print(f"Faithfulness: {total_matched}/{total_chunks} = {total_matched/total_chunks:.1%}")


if __name__ == "__main__":
    eval_retrieval()
    eval_faithfulness()
