from os import path
from secrets import token_hex
from sqlite3 import Connection


db_schema_file  = 'schema.sql'
db_file         = 'database.db'
secret          = ''


if not path.isfile(db_schema_file):
    print(f'No database schema file "{db_schema_file}". Exiting...')
    exit()


if not path.isfile(db_file):
    with open(db_schema_file, 'r') as file:
        script = file.read()
    print(script)
    with Connection(db_file) as conn:
        conn.executescript(script)


if path.isfile('secret.txt'):
    with open('secret.txt', 'r') as file:
        secret = file.read()
else:
    secret = token_hex(16)
    with open('secret.txt', 'w') as file:
        file.write(secret)