from fastapi import FastAPI

app = FastAPI(
    title="CastleWatch",
    description="Self-hosted security monitoring and incident response platform.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "name": "CastleWatch",
        "version": "0.1.0",
        "status": "online",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }