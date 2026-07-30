from fastapi import FastAPI

app = FastAPI(
    title="WebTrust API",
    version="0.1.0"
)

@app.get("/")
def root():
    return {
        "application": "WebTrust",
        "status": "running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }