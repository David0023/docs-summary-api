from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn

from api.auth import router as auth_router
from api.v1.routers import router as v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # DB initialisation should be done with alembic.
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(v1_router)


@app.get("/")
async def read_docs():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
