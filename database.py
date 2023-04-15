import sys
from cs50 import SQL

is_testing = 'pytest' in sys.argv[0]

test_db = "sqlite:///test.db"
develop_db = "sqlite:///project.db"

db_name = test_db if is_testing else develop_db
print(f'database in use => {db_name}')

db = SQL(db_name)