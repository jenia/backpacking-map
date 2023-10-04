import fastapi

from app import db


class HTTPServer:
    def __init__(self, db):
        self._router: fastapi.APIRouter = fastapi.APIRouter()
        self._db0 = db
        self._router.add_api_route(
            "/hero/{hero_name}",
            self.get_hero_endpoint,
            methods=["GET"],
        )
        self._router.add_api_route(
            "/hero", self.post_hero_endpoint, methods=["POST"], status_code=201
        )
        self._router.add_api_route(
            "/version",
            self.get_version,
            methods=["GET"],
        )

    def get_hero_endpoint(self, hero_name: str):
        hero = db.get_hero(hero_name, self._db0)
        return hero

    async def post_hero_endpoint(self, hero: db.Hero):
        db.insert_hero(hero, self._db0)

    async def get_version(self):
        return {"version": "1"}
