from fastapi import FastAPI

from db.session import create_all
from models import company  # noqa: F401  (registers Company on Base.metadata)

app = FastAPI(title="GaskeunKerja for Business — MVP")


@app.on_event("startup")
def on_startup():
    create_all()


@app.get("/health")
def health():
    return {"status": "ok"}
