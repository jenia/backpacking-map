import unittest
from functools import wraps

import psycopg2

import app.db as db

"""
TODO: These tests will fail in the pipeline because of the `host`.
      This means that we need to resolve the postgres host using DNS and if
      that fails, use localhost. This way, the tests will pass both during
      local development and in the pipeline.

      This will further fail in the pipeline because we're using an empty
      password. It's working on the localhost because we're tunneling to the
      Postgresql pod and the Postgresql docker image is configured to allow
      connection from localhost without a password. This will obviously fail in
      the pipeline as it should.
"""


class TestInitializeDatabase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database_wanted = "test00"
        self.table_name_wanted = "test_example_table_00"

    @staticmethod
    def setup_db_finally_close_conn():
        def _setup_db_finally_close_conn(test_func):
            @wraps(test_func)
            def wrap(self, *args, **kwargs):
                conn = None
                conn = psycopg2.connect(
                    host="127.0.0.1", user="postgres", dbname=self.database_wanted
                )
                conn.autocommit = True
                try:
                    db.create_database_if_not_exists(
                        "127.0.0.1", self.database_wanted, "postgres", ""
                    )
                    db.create_example_table_if_not_exists(
                        "127.0.0.1",
                        self.database_wanted,
                        self.table_name_wanted,
                        "postgres",
                        "",
                    )
                    test_func(self, conn)
                finally:
                    if conn:
                        conn.close()

            return wrap

        return _setup_db_finally_close_conn

    def test_database_creation(self):
        """test given database not in postgres then create it"""
        conn = None
        conn = psycopg2.connect(host="127.0.0.1", user="postgres")
        conn.autocommit = True

        try:
            with conn.cursor() as cur0:
                # prepare
                cur0.execute(
                    (
                        "select from pg_database where datname"
                        + f" = '{self.database_wanted}'"
                    )
                )
                rows = cur0.fetchall()
                if len(rows) != 0:
                    cur0.execute(f"DROP DATABASE {self.database_wanted}")

                # test
                db.create_database_if_not_exists(
                    "127.0.0.1", self.database_wanted, "postgres", ""
                )

                # verify
                cur0.execute(
                    "select from pg_database where datname"
                    + f" ='{self.database_wanted}'"
                )
                rows = cur0.fetchall()
                if len(rows) != 1:
                    failMsg = f"database {self.database_wanted} does not exist"
                    self.fail(failMsg)
        finally:
            if conn:
                conn.close()

    @setup_db_finally_close_conn()
    def test_create_table(self, conn):
        """Given table not in database when creating table then table created
        in db
        """
        with conn.cursor() as cur0:
            # prepare
            cur0.execute(f"DROP TABLE IF EXISTS {self.table_name_wanted}")

            # test
            db.create_example_table_if_not_exists(
                "127.0.0.1",
                self.database_wanted,
                self.table_name_wanted,
                "postgres",
                "",
            )

            # verify
            sql = (
                "select * from information_schema.tables where table_name = "
                + f"'{self.table_name_wanted}';"
            )

            print(sql)
            cur0.execute(sql)
            rows = cur0.fetchall()

            lenRows = len(rows)
            print(f"\n\n len rows: {lenRows}")
            if len(rows) != 1:
                self.fail(f"table {self.table_name_wanted} does not exist")

