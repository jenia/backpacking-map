from app.db.hero import DB, Hero, get_hero, insert_hero


def test_insert_hero():
    """Given table and database exist when inserting hero then data is written to
    db
    """
    DB()
    name = 'Evgeniy'
    age = 37
    h0 = Hero(name=name, secret_name="jenia", age=age)
    insert_hero(h0)

    hero_got = get_hero(name=name)

    assert hero_got is not None
    assert hero_got.age == age

    print("was here")
