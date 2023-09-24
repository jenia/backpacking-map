from app.db.initialize import DB
from app.http.endpoints import get_http_server

DB()
app = get_http_server
