"""FastAPI 服务：暴露 /query 接口。"""

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

from executor import execute


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    sql: str
    columns: list[str]
    rows: list[list]
    error: str | None = None


app = FastAPI(title="SQL 数据分析 Agent")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    result = execute(req.question)
    return QueryResponse(
        sql=result["sql"],
        columns=result["columns"],
        rows=result["rows"],
        error=result["error"],
    )


app.mount("/", StaticFiles(directory=str(ROOT / "static"), html=True), name="static")