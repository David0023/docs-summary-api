from fastapi import APIRouter
from api.v1.jobs import router as jobs_router
from api.v1.documents import router as documents_router

router = APIRouter(
    prefix="/api/v1",
    tags=["v1"]
)

router.include_router(jobs_router)
router.include_router(documents_router)