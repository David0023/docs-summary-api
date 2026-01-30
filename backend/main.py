from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from utils.database import engine, Base

from api.auth import router as auth_router
from api.v1.routers import router as v1_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(v1_router)

# Create all database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
async def read_docs():
    return RedirectResponse(url="/docs")