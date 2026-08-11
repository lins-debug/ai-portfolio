"""FastAPI 服务：暴露 /ask 接口。"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from retriever import retrieve
from generator import generate, build_prompt


class AskRequest(BaseModel):
    question: str
    top_k: int = 3
    include_answer: bool = True


class SourceItem(BaseModel):
    source: str
    title: str
    text: str
    similarity: float


class AskResponse(BaseModel):
    answer: str | None = None
    sources: list[SourceItem]


app = FastAPI(title="RAG 求职知识库助手")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def _startup():
    load_dotenv(ROOT / ".env")


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    results = retrieve(req.question, req.top_k)

    sources = [
        SourceItem(
            source=item["metadata"]["source"],
            title=item["metadata"]["title"],
            text=item["text"],
            similarity=round(1.0 - item["distance"], 3),
        )
        for item in results
    ]

    answer = None
    if req.include_answer:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise HTTPException(500, "未配置 OPENAI_API_KEY")
        answer = generate(req.question, results)

    return AskResponse(answer=answer, sources=sources)


# 托管前端静态文件（需要放在 server.py 下方）
app.mount("/", StaticFiles(directory=str(ROOT / "static"), html=True), name="static")