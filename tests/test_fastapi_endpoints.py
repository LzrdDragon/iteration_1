from fastapi.testclient import TestClient

import asgi
from iteration_1.entities import LinksRequest
from iteration_1.fastapi_endpoints import URLs


client = TestClient(asgi.app)


def test_post_links_inner_pool():
    links = ["https://huawei-krsk.ru", "https://google.com"]
    links_list = LinksRequest(links=links).dict()
    response = client.post(
        URLs.post_links.value,
        json=links_list,
    )
    assert response.status_code == 200
    assert response.json() == {
        "links": [
            {
                "link": "https://huawei-krsk.ru",
                "title": "\n        \nОфициальный магазин HUAWEI в Красноярске\n\n    ",
            },
            {"link": "https://google.com", "title": "Google"},
        ]
    }


def test_post_links_upper_pool():
    links = ["https://huawei-krsk.ru", "https://google.com"]
    links_list = LinksRequest(links=links).dict()
    response = client.post(
        URLs.post_links_upper.value,
        json=links_list,
    )
    assert response.status_code == 200
    assert response.json() == {
        "links": [
            {
                "link": "https://huawei-krsk.ru",
                "title": "\n        \nОфициальный магазин HUAWEI в Красноярске\n\n    ",
            },
            {"link": "https://google.com", "title": "Google"},
        ]
    }
