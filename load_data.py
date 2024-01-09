import hashlib
import sqlite3
import json
import sys

salt = "library"

con = sqlite3.connect("datos.db")
cur = con.cursor()

# Create tables
cur.execute("""
    CREATE TABLE Author(
        id integer primary key AUTOINCREMENT,
        name varchar(40)
    )
""")

cur.execute("""
    CREATE TABLE Book(
        id integer primary key AUTOINCREMENT,
        title varchar(50),
        author integer,
        cover varchar(50),
        description TEXT,
        numCopies integer,
        FOREIGN KEY(author) REFERENCES Author(id)
    )
""")

cur.execute("""
    CREATE TABLE User(
        id integer primary key AUTOINCREMENT,
        name varchar(20),
        email varchar(30),
        password varchar(32)
    )
""")

cur.execute("""
    CREATE TABLE Request(
        requestDate datetime,
        accepted boolean,
        requesterUserId integer, 
        requestedUserId integer,
        PRIMARY KEY(requesterUserId, requestedUserId),
        FOREIGN KEY(requesterUserId) REFERENCES User(id),
        FOREIGN KEY(requestedUserId) REFERENCES User(id)
    )
""")

cur.execute("""
    CREATE TABLE Reserve(
        returned boolean,
        userId integer,
        bookId integer,
        reserveDate datetime,
        PRIMARY KEY(userId, bookId, reserveDate),
        FOREIGN KEY(userId) REFERENCES User(id),
        FOREIGN KEY(bookId) REFERENCES Book(id)
    )
""")

cur.execute("""
    CREATE TABLE Review(
        rating integer,
        comment varchar,
        userId integer,
        bookId integer,
        PRIMARY KEY(userId, bookId),
        FOREIGN KEY(userId) REFERENCES User(id),
        FOREIGN KEY(bookId) REFERENCES Book(id)
    )
""")

cur.execute("""
    CREATE TABLE Session(
        session_hash varchar(32) primary key,
        user_id integer,
        last_login float,
        FOREIGN KEY(user_id) REFERENCES User(id)
    )
""")

# Insert users

with (open('usuarios.json', 'r') as f):
    usuarios = json.load(f)['usuarios']

for user in usuarios:
    dataBase_password = user['password'] + salt
    hashed = hashlib.md5(dataBase_password.encode())
    dataBase_password = hashed.hexdigest()
    cur.execute(f"""INSERT INTO User VALUES (NULL, '{user['nombres']}', '{user['email']}', '{dataBase_password}')""")
    con.commit()

# Insert books
with open('libros_short.tsv', 'r') as f:
    libros = [x.split("\t") for x in f.readlines()]

author_id = 0
for author, title, cover, description in libros:
    res = cur.execute(f"SELECT id FROM Author WHERE name=\"{author}\"")
    if len(res.fetchall()) == 0:
        cur.execute(f"""INSERT INTO Author VALUES (NULL, \"{author}\")""")
        con.commit()
        res = cur.execute(f"SELECT id FROM Author WHERE name=\"{author}\"")
        author_id = res.fetchone()[0]

    cur.execute("INSERT INTO Book VALUES (NULL, ?, ?, ?, ?, 10)",
                (title, author_id, cover, description.strip()))

    con.commit()

cur.execute("Insert into Request Values (datetime('now'),false,1,2)")
cur.execute("Insert into Request Values (datetime('now'),true,4,3)")
cur.execute("Insert into Reserve Values (false,1,87,datetime('now'))")
cur.execute("Insert into Reserve Values (false,4,243,datetime('now'))")
cur.execute("Insert into Review Values (7,'Commentary',2,492)")
cur.execute("Insert into Review Values (3,'Commentary',1,237)")
con.commit()

sys.exit(0)
