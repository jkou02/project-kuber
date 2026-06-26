"""Entrypoint de FastAPI."""

from fastapi import FastAPI

app = FastAPI(title="KuberCalc API", version="0.1.0")


@app.get("/health")
async def health_check() -> dict:
    return {"status": "ok"}
