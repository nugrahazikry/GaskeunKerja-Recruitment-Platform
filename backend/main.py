from fastapi import FastAPI

app = FastAPI(title="GaskeunKerja for Business — MVP")


@app.get("/health")
def health():
    return {"status": "ok"}
