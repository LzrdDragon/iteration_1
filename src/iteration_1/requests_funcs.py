import requests
from bs4 import BeautifulSoup


def get_title_sync(link: str) -> str:
    html = requests.get(link).text
    soup = BeautifulSoup(html, "lxml")
    title = str(soup.find("title").text)
    return title
