from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "working"}

@app.get("/health")
def health():
    return "OK"
