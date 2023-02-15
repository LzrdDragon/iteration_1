from typing import List
import uuid

from pydantic.dataclasses import dataclass
from pydantic import BaseModel, PrivateAttr


class Link(BaseModel):
    link: str
    _id: uuid.UUID = PrivateAttr(default_factory=uuid.uuid4)

    class Config:
        extra = 'forbid'

        schema_extra = {"link": "https://example.ru"}


class LinksList(BaseModel):
    links: List[Link]

    class Config:
        extra = 'forbid'

        schema_extra = {
            "links": [
                {"link": "https://example.ru"},
                {"link": "https://example.com"}
            ]
        }


class LinkResponse(BaseModel):
    link: str
    title: str
    _id: uuid.UUID = PrivateAttr(default_factory=uuid.uuid4)

    class Config:
        extra = 'forbid'


class LinksListResponse(BaseModel):
    links: List[LinkResponse]

    class Config:
        extra = 'forbid'
