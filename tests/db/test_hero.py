from app import db


def test_insert_hero():
    """Given table and database exist when inserting hero then data is written to
    db
    """
    db0 = db.DB()
    name = "Evgeniy"
    age = 37

    h0 = db.Hero(name=name, secret_name="jenia", age=age)
    db.insert_hero(hero=h0, db=db0)

    hero_got = db.get_hero(name=name, db=db0)

    assert hero_got is not None
    assert hero_got.age == age
