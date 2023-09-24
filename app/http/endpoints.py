from collections.abc import Callable

from fastapi import FastAPI

from app.db.hero import Hero, get_hero, insert_hero

http_server = FastAPI()

insert_hero_inter: Callable[[Hero], None] = insert_hero
get_hero_inter: Callable[[str], Hero | None] = get_hero

@http_server.get("/hero/{hero_name}")
async def get_hero_endpoint(name: str):
    hero = get_hero_inter(name)
    return hero


@http_server.post("/hero")
async def post_hero_endpoint(hero: Hero):
    insert_hero_inter(hero)
    return hero


def get_http_server() -> FastAPI:
    return http_server
