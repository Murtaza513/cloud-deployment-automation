import os
from contextlib import asynccontextmanager

import psycopg
from fastapi import FastAPI
from pydantic import BaseModel


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://appuser:change-me-in-production@localhost:5432/appdb",
)


class MessageCreate(BaseModel):
    text: str


def psycopg_url() -> str:
    return DATABASE_URL.replace("postgresql+psycopg://", "postgresql://")


def init_db() -> None:
    if os.getenv("SKIP_DB_INIT") == "true":
        return

    with psycopg.connect(psycopg_url()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    text TEXT NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
                """
            )


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="DevOps Portfolio API",
    description="FastAPI service deployed with Terraform, Ansible, Docker, and PostgreSQL.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def read_root():
    return {
        "service": "DevOps Portfolio API",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/messages", status_code=201)
def create_message(payload: MessageCreate):
    with psycopg.connect(psycopg_url()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO messages (text) VALUES (%s) RETURNING id, text, created_at",
                (payload.text,),
            )
            row = cur.fetchone()

    return {"id": row[0], "text": row[1], "created_at": row[2].isoformat()}


@app.get("/messages")
def list_messages():
    with psycopg.connect(psycopg_url()) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, text, created_at FROM messages ORDER BY id DESC")
            rows = cur.fetchall()

    return [
        {"id": row[0], "text": row[1], "created_at": row[2].isoformat()}
        for row in rows
    ]
