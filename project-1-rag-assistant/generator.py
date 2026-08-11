"""答案生成：把检索结果拼成 prompt，调 LLM 出答案。"""

import os
from pathlib import Path

from openai import OpenAI

ROOT = Path(__file__).resolve().parent


def _get_client() -> OpenAI:
    return OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    )


def build_prompt(question: str, results: list[dict]) -> str:
    context_parts = []
    for item in results:
        meta = item["metadata"]
        context_parts.append(
            f"[来源: {meta['source']} / {meta['title']}]\n{item['text']}"
        )
    context = "\n\n".join(context_parts)

    return (
        '请只根据下面资料回答问题。如果资料不足，请明确说"资料中没有提到"。\n\n'
        f"## 资料\n{context}\n\n"
        f"## 用户问题\n{question}"
    )


def generate(question: str, results: list[dict]) -> str:
    client = _get_client()
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": "你是严谨的中文 RAG 助手。只使用资料中的事实，不编造来源。"},
            {"role": "user", "content": build_prompt(question, results)},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()
