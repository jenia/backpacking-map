from unittest import mock
import pdb
import httpx
from fastapi import FastAPI, testclient

from app import db, http


class HeroDBMock:
    def __init__(self, hero: db.Hero):
        self.hero_named_called: str = ""
        self.hero: db.Hero = hero

    def get_hero_mock(self, name: str, _: db.DB) -> db.Hero | None:
        self.hero_named_called = name
        return self.hero

    def insert_hero_mock(self, hero: db.Hero, _: db.DB) -> None:
        self.hero = hero

def test_get_hero():
    """Given hero exists, when GET hero, then return hero from DB"""
    expected_hero = db.Hero(name="Eugene", secret_name="jenia")
    db_mock = HeroDBMock(hero=expected_hero)
    patcher = mock.patch("app.db.get_hero", db_mock.get_hero_mock)
    patcher.start()
    server = http.HTTPServer(db_mock)
    app = FastAPI()
    app.include_router(server._router)
    tc = testclient.TestClient(app)
    resp = tc.get("/hero/eugene")
    assert resp.status_code is int(httpx.codes.OK)
    hero_got = db.Hero(**resp.json())
    assert hero_got.secret_name == expected_hero.secret_name


def test_post_hero():
    """Given hero does not exist, when POST heor, then DB is called to insert
    """
    expected_hero = db.Hero(name="Eugene", secret_name="jenia")
    db_mock = HeroDBMock(hero=expected_hero)
    patcher = mock.patch("app.db.insert_hero", db_mock.insert_hero_mock)
    patcher.start()
    server = http.HTTPServer(db_mock)
    app = FastAPI()
    app.include_router(server._router)
    tc = testclient.TestClient(app)
    resp = tc.post("/hero", json=expected_hero.dict())
    assert resp.status_code == int(httpx.codes.CREATED)
    assert db_mock.hero.secret_name == expected_hero.secret_name
