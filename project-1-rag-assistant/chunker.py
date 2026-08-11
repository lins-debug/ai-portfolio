def chunk_markdown(text: str, source: str) -> list[dict]:
    """将一篇 Markdown 文本切分为标题级 chunk。

    每个 chunk 包含 id、source、title、text 四个字段。
    """
    chunks: list[dict] = []
    title = source
    lines: list[str] = []

    def flush():
        """把当前攒的行打包成一个 chunk，然后清空。"""
        body = "\n".join(lines).strip()
        if body:
            chunks.append({
                "id": f"{source}:{len(chunks)}",
                "source": source,
                "title": title,
                "text": body,
            })
        lines.clear()

    for line in text.splitlines():
        if line.startswith("#"):
            flush()
            title = line.lstrip("#").strip() or source
        elif line.strip():
            lines.append(line.strip())

    flush()
    return chunks
