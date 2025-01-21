from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from core.dependencies import auth
from models.models import ProcessTextRequest, ProcessTextResponse
from services.service import ProcessedTextServiceError

router = APIRouter(dependencies=[Depends(auth)])


@router.post("/process-text", response_model=ProcessTextResponse)
async def process_text(body: ProcessTextRequest, request: Request) -> Body:
    try:
        return await request.app.service.create_process_resp(req=body)
    except ProcessedTextServiceError:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/processed-texts", response_model=List[ProcessTextResponse])
async def get_processed_texts(request: Request, offset: int = 0, limit: int = 50) -> Body:
    try:
        return await request.app.service.get_processes(offset=offset, limit=limit)
    except ProcessedTextServiceError:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)
