import psycopg2
import os

connection = psycopg2.connect(os.getenv('DATABASE_URL'))
connection.autocommit = True

with connection.cursor() as cur:
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        name varchar(255) NOT NULL,
        email varchar(255) PRIMARY KEY,
        password varchar(255) NOT NULL,
        type varchar(255) NOT NULL
    )''')

users = [
    ("Elev 5436", "elev5436@skola.se", "Sommar2021", "student"),
    ("Klas Klasson", "klas.klasson@skola.se", "0u7_0f_c0ff33", "teacher")
]

for t in users:
    with connection.cursor() as cur:
        cur.execute('''INSERT INTO users (name, email, password, type)
            VALUES (%s, %s, %s, %s)''', t)

connection.close()
