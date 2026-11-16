from fastapi import FastAPI

app = FastAPI(title="finance-app API")

@app.get("/health")
def health() -> dict[str,str]:
    return {"status":"ok"}