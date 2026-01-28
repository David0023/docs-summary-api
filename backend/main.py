from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from utils.database import engine, Base

from api.auth import router as auth_router

app = FastAPI()
app.include_router(auth_router)

# Create all database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
async def read_docs():
    return RedirectResponse(url="/docs")