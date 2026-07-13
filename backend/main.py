from fastapi import FastAPI

import models  # noqa: F401  (registers all models on Base.metadata)
from db.session import create_all
from db.vector_store import create_collections
from routers import auth, candidates, interview_answers, interview_questions, jobs, matching

app = FastAPI(title="GaskeunKerja for Business — MVP")
app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(candidates.router)
app.include_router(matching.router)
app.include_router(interview_questions.router)
app.include_router(interview_answers.router)


@app.on_event("startup")
def on_startup():
    create_all()
    create_collections()


@app.get("/health")
def health():
    return {"status": "ok"}
