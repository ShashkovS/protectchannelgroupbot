# Для работы по виндой нужны PYTHONUTF8=1
import os
from unittest import TestCase
from datetime import datetime

from helpers.consts import *
import db_methods as db


class DatabaseMethodsTest(TestCase):
    def setUp(self) -> None:
        print(f'setup, id={id(self)}, {self!r}')
        self.db = db
        test_db_filename = f'../db/unittest.db'
        # ensure there is no trash file from previous incorrectly handled tests present
        for file in [test_db_filename, test_db_filename + '-shm', test_db_filename + '-wal']:
            try:
                os.unlink(file)
            except FileNotFoundError:
                pass
        # create shiny new db instance from scratch and connect
        self.db.sql.setup(test_db_filename)
        # Making it blazing fast
        self.db.sql.conn.execute('''      PRAGMA journal_mode = OFF;       ''')
        self.db.sql.conn.execute('''      PRAGMA synchronous = 0;       ''')
        self.db.sql.conn.execute('''      PRAGMA cache_size = 1000000;       ''')
        self.db.sql.conn.execute('''      PRAGMA locking_mode = EXCLUSIVE;       ''')
        self.db.sql.conn.execute('''      PRAGMA temp_store = MEMORY;       ''')

    def tearDown(self) -> None:
        print(f'tearDown, id={id(self)}')
        self.db.sql.disconnect()
        try:
            os.unlink(self.db.sql.db_file)
        except PermissionError:
            pass


    def test_users_add_and_fetch_all(self):
        pass
