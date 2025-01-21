from fastapi import APIRouter

from api.handlers import router as process_text_router

router = APIRouter()

router.include_router(router=process_text_router, prefix="", tags=["process-text"])
