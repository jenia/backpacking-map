import fastapi
import opentelemetry.sdk.trace as ot_trace
import opentelemetry.sdk.trace.export as ot_export
from opentelemetry import trace

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
        trace.set_tracer_provider(ot_trace.TracerProvider())
        trace.get_tracer_provider().add_span_processor(
            ot_export.BatchSpanProcessor(ot_export.ConsoleSpanExporter())
        )
        self.tracer = trace.get_tracer(__name__)

    def get_hero_endpoint(self, hero_name: str):
        with self.tracer.start_as_current_span("foo"):
            hero = db.get_hero(hero_name, self._db0)
            return hero

    async def post_hero_endpoint(self, hero: db.Hero):
        db.insert_hero(hero, self._db0)

    async def get_version(self):
        return {"version": "1"}
