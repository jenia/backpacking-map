import typing

import sqlmodel

from .initialize import DB


class Hero(sqlmodel.SQLModel, table=True):
    id: typing.Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None


def insert_hero(hero: Hero, db: DB) -> None:
    with sqlmodel.Session(db._ENG_) as session:
        session.add(hero)
        session.commit()


def get_hero(name: str, db: DB) -> Hero | None:
    with sqlmodel.Session(db._ENG_) as session:
        stm = sqlmodel.select(Hero).where(Hero.name == name)
        hero = session.exec(stm).first()
        return hero
