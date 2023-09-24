import psycopg2
from sqlalchemy.engine import URL
from sqlmodel import SQLModel, create_engine


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
        global _ENG_
        _ENG_ = create_engine(url_object)
        SQLModel.metadata.create_all(_ENG_)


def create_database_if_not_exists(host, db_name, username, passwd):
    conn = None
    try:
        conn = psycopg2.connect(host=host, user=username, password=passwd)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(f"select from pg_database where datname = '{db_name}'")
            if len(cur.fetchall()) == 0:
                cur.execute(f"CREATE DATABASE {db_name}")
    except Exception as err:
        print("DB error:", err)
        raise err
    finally:
        if conn:
            conn.close()


def create_example_table_if_not_exists(host, db_name, table, username, passwd):
    conn = None
    try:
        conn = psycopg2.connect(
            host=host, user=username, password=passwd, dbname=db_name
        )
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(
                f"CREATE TABLE IF NOT EXISTS {table}"
                + " (id serial PRIMARY KEY, num integer, data varchar);"
            )
    except Exception as err:
        print("DB error:", err)
        raise err
    finally:
        if conn:
            conn.close()
