from typing import List

from aioredis import Redis

from models.models import ProcessTextResponse


class ProcessedTextRepoError(Exception):
    def __init__(self, msg, *args):
        self.msg = msg
        super().__init__(*args)


class ProcessedTextRepo:
    def __init__(self, redis_cli: Redis):
        self._redis = redis_cli

    async def get_list(self, offset: int | None = None, limit: int | None = None) -> List[ProcessTextResponse]:
        try:
            res = await self._redis.lrange("events", offset, offset + limit - 1)
        except:
            raise ProcessedTextRepoError("redis client error")
        return [ProcessTextResponse.model_validate_json(item) for item in res]

    async def create(self, item: ProcessTextResponse) -> ProcessTextResponse:
        try:
            await self._redis.rpush("events", item.model_dump_json())
        except:
            raise ProcessedTextRepoError("redis client error")

        return item
