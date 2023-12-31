import logging

import uvicorn
from fastapi import FastAPI

from app import db, http

FORMAT = '%(levelname)s: %(asctime)s %(pathname)s:%(lineno)d %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

db0 = db.DB()
server = http.HTTPServer(db0)
app = FastAPI()
app.include_router(server._router)


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=False)


if __name__ == "__main__":
    start()
