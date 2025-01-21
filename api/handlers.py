from typing import List

from fastapi import APIRouter, Body, Request

from models.models import ProcessTextRequest, ProcessTextResponse

router = APIRouter()


@router.post("/process-text", response_model=ProcessTextResponse)
async def process_text(body: ProcessTextRequest, request: Request) -> Body:
    return await request.app.service.create_process_resp(req=body)


@router.get("/processed-texts", response_model=List[ProcessTextResponse])
async def get_processed_texts(request: Request, offset: int = 0, limit: int = 50) -> Body:
    return await request.app.service.get_processes(offset=offset, limit=limit)
