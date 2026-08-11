"""一键入库：读取 data/ 下所有 .md，切分后存入 Chroma。"""

import os
from pathlib import Path

from dotenv import load_dotenv

from chunker import chunk_markdown
from vector_store import add_chunks

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"


def main():
    # 加载环境变量（.env 里的 API Key 等）
    load_dotenv(ROOT / ".env")

    all_chunks: list[dict] = []
    md_files = sorted(DATA_DIR.glob("*.md"))

    if not md_files:
        print("data/ 目录下没有 .md 文件。")
        return 1

    for path in md_files:
        text = path.read_text(encoding="utf-8")
        chunks = chunk_markdown(text, path.name)
        all_chunks.extend(chunks)
        print(f"  {path.name} → {len(chunks)} 个 chunk")

    add_chunks(all_chunks)
    print(f"\n总计 {len(all_chunks)} 个 chunk 已入库。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())