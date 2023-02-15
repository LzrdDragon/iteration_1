from __future__ import annotations
import enum
import json
import os
import logging
from logging.config import dictConfig

from fastapi import APIRouter

from .entities import Link, LinksList, LinkResponse, LinksListResponse
from .aiohttp_funcs import get_title
from .config import LogConfig

# adding custom logger
dictConfig(LogConfig().dict())
logger = logging.getLogger("iteration_1")

# initializing api router
router = APIRouter()


# setting up api urls
class URLs(str, enum.Enum):
    post_links = "/iteration_1/post-links"
    post_link = "/iteration_1/post-link"


# post endpoint for one link
@router.post(
    URLs.post_link.value,
    name="post_link",
    summary="Post Link - Get Tittle",
    response_model=LinkResponse,
)
async def post_link(link: Link):
    title = await get_title(link.link)
    response = LinkResponse(link=link.link, title=title)
    return response


# post endpoint for several links
@router.post(
    URLs.post_links.value,
    name="post_links",
    summary="Post a List of Links - Get Links with Tittles",
    response_model=LinksListResponse,
)
async def post_links(links_list: LinksList | str):
    if type(links_list) == str:
        links_list = json.loads(links_list)
        links_list = LinksList(links=links_list["links"])
    else:
        links_list = LinksList(links=links_list.links)

    # creating an empty response and filling it up
    response = LinksListResponse(links=[])
    for link in links_list.links:
        title = await get_title(link.link)
        link_response = LinkResponse(link=link.link, title=title)
        response.links.append(link_response)

    return response


if __name__ == "__main__":
    print(
        f"A fastapi_endpoints.py module from {os.getcwd()} has just ran as a __main__"
    )
