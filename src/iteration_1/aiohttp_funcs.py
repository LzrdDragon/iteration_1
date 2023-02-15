import asyncio
from typing import List

import aiohttp
from fastapi.encoders import jsonable_encoder
from bs4 import BeautifulSoup

from iteration_1.entities import LinksList, Link


# go to the given url and return its html title
async def get_title(link: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'lxml')
            title = str(soup.find('title').text)
            return title


# post one url to an api endpoint
async def post_link_to_api(link: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://127.0.0.1:8000/iteration_1/post-link",
            json=jsonable_encoder(Link(link=link)),
        ) as response:
            link_title = await response.text()
            print(response.status)
            print(link_title)
            return link_title


# post several urls to an api endpoint
async def post_links_to_api(urls: List[str]):
    links = []
    for url in urls:
        links.append(Link(link=url))
    links = LinksList(links=links).json()
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://127.0.0.1:8000/iteration_1/post-links",
            json=links
        ) as response:
            links_titles = await response.text()
            print(response.status)
            print(links_titles)
            return links_titles


if __name__ == '__main__':
    asyncio.run(post_link_to_api("https://huawei-krsk.ru"))
    asyncio.run(post_links_to_api(["https://huawei-krsk.ru", "https://google.com"]))
