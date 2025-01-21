from typing import TypeVar

from faker import Faker
from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import BaseModel

from models.models import ProcessTextRequest, ProcessTextResponse

fake = Faker()

T = TypeVar("T", bound=BaseModel)


class ProcessTextResponseFactory(ModelFactory):
    __faker__ = fake
    __model__ = ProcessTextResponse


class ProcessTextRequestFactory(ModelFactory):
    __faker__ = fake
    __model__ = ProcessTextRequest
