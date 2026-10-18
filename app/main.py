from fastapi import FastAPI

app = FastAPI(title="TinyOps Status API")


@app.get("/")
def read_root():
    return {
        "message": "TinyOps Status API",
        "health": "/health",
    }


@app.get("/health")
def read_health():
    return {"status": "ok"}
