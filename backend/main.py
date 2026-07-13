from fastapi import FastAPI

import models  # noqa: F401  (registers all models on Base.metadata)
from db.session import create_all
from db.vector_store import create_collections

app = FastAPI(title="GaskeunKerja for Business — MVP")


@app.on_event("startup")
def on_startup():
    create_all()
    create_collections()


@app.get("/health")
def health():
    return {"status": "ok"}
