from os import path
from secrets import token_hex


db_schema_file  = 'schema.sql'
if not path.isfile(db_schema_file):
    print(f'No database schema file "{db_schema_file}". Exiting...')
    exit()
db_file         = 'database.db'

secret          = ''
if path.isfile('secret.txt'):
    with open('secret.txt', 'r') as file:
        secret = file.read()
else:
    secret = token_hex(16)
    with open('secret.txt', 'w') as file:
        file.write(secret)