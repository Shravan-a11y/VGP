from fastapi import FastAPI
from app.core.config import settings

app=FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION
    )

@app.get("/")
async def root():
    return  {
    "Message":"Visitor gate Passing"
    }