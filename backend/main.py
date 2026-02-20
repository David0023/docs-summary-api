from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from core.database import engine, Base
import uvicorn

from api.auth import router as auth_router
from api.v1.routers import router as v1_router

async def main():
    app = FastAPI()
    app.include_router(auth_router)
    app.include_router(v1_router)

    # Create all database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    @app.get("/")
    async def read_docs():
        return RedirectResponse(url="/docs")
    
if __name__ == "__main__":
    uvicorn.run(main(), host="0.0.0.0", port=8000)