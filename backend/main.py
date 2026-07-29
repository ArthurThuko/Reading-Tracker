from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Reading Tracker API"}

@app.get("/status")
async def read_status():
    return {"status": "ok"}


@app.get("/about")
async def read_about():
    return {
        "project": "This API allows users to track their reading progress and manage their reading lists.",
        "author": "Arthur Henrique",
    }