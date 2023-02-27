from __future__ import annotations
import enum
import sys
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor
from math import ceil

from fastapi import APIRouter

from iteration_1.entities import LinksRequest, LinksResponse, LinkParsed
from iteration_1.aiohttp_funcs import get_title
from iteration_1.requests_funcs import get_title_sync
from iteration_1.structlog_config import log


# ProcessPoolExecutor из api endpoint'а, передавать лист в него через map с chunk size,
# равным количеству линок, делённых на number of worker processes
# И workers = cpu_count
# Добавлять линки в дикт и по ним потом передавать тайтлы
# Синхронизировать добавление тайтлов, то есть лочить дикт с линками, когда мы добавляем
# в него тайтл (mutex)

# initializing api router
router = APIRouter()


# setting up api urls
class URLs(str, enum.Enum):
    post_links = "/iteration_1/post-links"
    post_links_upper = "/iteration_1/post-links-upper"


# post endpoint for several links
@router.post(
    URLs.post_links.value,
    name="post_links",
    summary="Post a List of Links - Get Links with Tittles",
    response_model=LinksResponse,
)
async def post_links(links_list: LinksRequest):
    response = LinksResponse(links=[])
    for link in links_list.links:
        title = await get_title(link)
        link_response = LinkParsed(link=link, title=title)
        response.links.append(link_response)
    return response


# post endpoint for several links with process pool executor from here
# из-за chanksize, на большом количестве линок должно быстрее работать
@router.post(
    URLs.post_links_upper.value,
    name="post_links",
    summary="Post a List of Links - Get Links with Tittles",
    response_model=LinksResponse,
)
async def post_links_upper(links_list: LinksRequest):
    response = LinksResponse(links=[])
    # how many tasks we can put into each process of a pool
    chunks_size = ceil(len(links_list.links) / cpu_count())
    # separating the links_list and putting each part to the
    # independent process through a Process Pool Executor
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        temporary_map = dict(
            zip(
                links_list.links,
                executor.map(get_title_sync, links_list.links, chunksize=chunks_size),
            )
        )
    # synchronously adding prepared link-title pairs to a response
    for link in temporary_map.keys():
        link_response = LinkParsed(link=link, title=temporary_map[link])
        response.links.append(link_response)
    return response


if __name__ == "__main__":
    log.info(f"A {sys.modules[__name__]} has just ran")
