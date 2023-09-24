from typing import Optional

from sqlmodel import Field, Session, SQLModel, select

from app.db.initialize import _ENG_


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None


def insert_hero(hero: Hero) -> None:
    with Session(_ENG_) as session:
        session.add(hero)
        session.commit()


def get_hero(name: str) -> Hero | None:
    with Session(_ENG_) as session:
        stm = select(Hero).where(Hero.name == name)
        hero = session.exec(stm).first()
        return hero
