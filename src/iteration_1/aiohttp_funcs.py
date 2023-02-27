import asyncio
import sys
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count

import aiohttp
from bs4 import BeautifulSoup

from iteration_1.structlog_config import log


# sync cpu blocking operations
def parse_a_title(html):
    soup = BeautifulSoup(html, "lxml")
    return str(soup.find("title").text)


# endpoint
async def get_title(link: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            html = await response.text()
            loop = asyncio.get_running_loop()  # where is better to locate it?
            with ProcessPoolExecutor(max_workers=cpu_count()) as pool:
                title = await loop.run_in_executor(pool, parse_a_title, html)
            return title


if __name__ == "__main__":
    log.info(f"A {sys.modules[__name__]} has just ran")
