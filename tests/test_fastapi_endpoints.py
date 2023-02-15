from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder

import asgi
from iteration_1.entities import Link, LinksList


client = TestClient(asgi.app)


def test_post_one_link():
    response = client.post(
        "http://127.0.0.1:8000/iteration_1/post-link",
        json=jsonable_encoder(Link(link="https://google.com")),
    )
    assert response.status_code == 200
    assert response.json() == {"link": "https://google.com", "title": "Google"}


def test_post_many_links():
    links = [Link(link="https://huawei-krsk.ru"), Link(link="https://google.com")]
    links_list = LinksList(links=links).json()
    response = client.post(
        "http://127.0.0.1:8000/iteration_1/post-links",
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
