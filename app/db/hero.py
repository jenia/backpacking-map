from typing import Optional
from app.db import create_database_if_not_exists
from sqlalchemy.engine import URL
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None

def insert_hero(hero: Hero) -> None:
    with Session(__ENG__) as session:
        session.add(hero)
        session.commit()

def get_hero(name: str) -> Hero | None:
    with Session(__ENG__) as session:
        stm = select(Hero).where(Hero.name == name)
        hero = session.exec(stm).first()
        return hero

class DB:
    def __init__(
        self, host="127.0.0.1", database="test00", username="postgres", password=""
    ):
        url_object = URL.create(
            "postgresql+psycopg2",
            username=username,
            password=password,
            host=host,
            database=database,
        )

        create_database_if_not_exists(host, database, username, password)
        global __ENG__
        __ENG__ = create_engine(url_object)
        SQLModel.metadata.create_all(__ENG__)
