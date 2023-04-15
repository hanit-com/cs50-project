from cs50 import SQL
from database import test_db


def pytest_sessionfinish(session, exitstatus):
    print(f"All tests are done, exit status = {exitstatus}")
    session.config.cache.max_entries = 0
    clear_tables()


def clear_tables():
    db = SQL(test_db)
    tables = ["users", "collections", "cards"]

    for table in tables:
        db.execute("DELETE FROM ?", table)