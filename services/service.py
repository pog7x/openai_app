from typing import List

from clients.openai_client import OpenAICLient
from models.models import ProcessTextRequest, ProcessTextResponse
from repositories.repository import ProcessedTextRepo, ProcessedTextRepoError


class ProcessedTextServiceError(Exception):
    def __init__(self, msg, *args):
        self.msg = msg
        super().__init__(*args)


class ProcessedTextService:
    def __init__(self, repo: ProcessedTextRepo, openai: OpenAICLient):
        self._repo: ProcessedTextRepo = repo
        self._openai = openai

    async def get_processes(self, offset: int | None = None, limit: int | None = None) -> List[ProcessTextResponse]:
        try:
            return await self._repo.get_list(offset=offset, limit=limit)
        except ProcessedTextRepoError as err:
            raise ProcessedTextServiceError(msg=err.msg)

    async def create_process_resp(self, req: ProcessTextRequest) -> ProcessTextResponse:
        try:
            resp = await self._openai.fetch_openai_response(prompt=req.payload.text)
        except ProcessedTextRepoError as err:
            raise ProcessedTextServiceError(msg=err.msg)

        res = ProcessTextResponse(
            event_id=req.event_id,
            request_text=req.payload.text,
            ai_response=resp,
        )

        try:
            return await self._repo.create(item=res)
        except ProcessedTextRepoError as err:
            raise ProcessedTextServiceError(msg=err.msg)
