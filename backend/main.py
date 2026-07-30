from fastapi import FastAPI
from app.routes import company
from app.routes import report

app = FastAPI(
    title="WebTrust API",
    version="0.1.0"
)

app.include_router(company.router)
app.include_router(report.router)

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