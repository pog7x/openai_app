from pydantic import BaseModel, Field


class ProcessTextPayload(BaseModel):
    text: str = Field(max_length=500)
    meta: dict


class ProcessTextRequest(BaseModel):
    event_id: str
    payload: ProcessTextPayload


class ProcessTextResponse(BaseModel):
    event_id: str
    request_text: str
    ai_response: str
