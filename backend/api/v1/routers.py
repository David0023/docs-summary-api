from fastapi import APIRouter
from api.v1.jobs import router as jobs_router

router = APIRouter(
    prefix="/api/v1",
    tags=["v1"]
)

router.include_router(jobs_router)