from pydantic import BaseModel, Field, Extra


class PydanticConfig(BaseModel):
    class Config:
        extra = Extra.allow


class LinksRequest(PydanticConfig):
    links: list[str] = Field(example=["http://example1.com", "https://example2.com"])


class LinkParsed(PydanticConfig):
    link: str
    title: str


class LinksResponse(PydanticConfig):
    links: list[LinkParsed]
