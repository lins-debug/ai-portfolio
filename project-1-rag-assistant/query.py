"""命令行查询：检索 + LLM 生成答案。"""

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv

from retriever import retrieve
from generator import generate

ROOT = Path(__file__).resolve().parent


def format_results(results: list[dict]) -> str:
    """格式化检索结果为可读文本。"""
    lines = []
    for i, item in enumerate(results, 1):
        meta = item["metadata"]
        dist = item["distance"]
        similarity = round(1.0 - dist, 3)
        lines.append(f"{i}. 【{similarity}】{meta['source']} / {meta['title']}")
        lines.append(f"   {item['text'][:100]}...")
    return "\n".join(lines)


def main():
    load_dotenv(ROOT / ".env")

    parser = argparse.ArgumentParser(description="RAG 求职知识库查询")
    parser.add_argument("question", nargs="?", help="要查询的问题")
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--no-llm", action="store_true", help="只检索，不调 LLM")
    args = parser.parse_args()

    question = args.question or input("请输入问题：")

    # 1. 检索
    results = retrieve(question, args.top_k)
    if not results:
        print("未检索到相关内容。")
        return 1

    print("=== 检索结果 ===")
    print(format_results(results))
    print()

    # 2. 如果只是调试检索，到此为止
    if args.no_llm:
        return 0

    # 3. 调 LLM 生成答案
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("未设置 OPENAI_API_KEY，跳过 LLM 生成。请检查 .env 文件。")
        return 0

    print("=== 答案 ===")
    answer = generate(question, results)
    print(answer)

    # 4. 列出来源
    print("\n=== 来源 ===")
    for item in results:
        meta = item["metadata"]
        print(f"- {meta['source']} / {meta['title']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())